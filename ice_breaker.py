from dotenv import load_dotenv


from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrap_linkedin_profile
from agents.linkedin_loopup_agent import lookup as linkedin_loopup_agent
from output_parser import summary_parser, Summary

def ice_breaker_with(name: str) -> tuple[Summary, str]:

    print("in ice_breaker_with function" + name)

    linkedin_url = linkedin_loopup_agent(name=name)
    linkedin_data = scrap_linkedin_profile(url=linkedin_url)

    if not linkedin_data:
        print(f" No LinkedIn data found for {name}. Returning empty summary.")
        return Summary(summary="No profile data found", facts=[]), None

    summary_template = """

    given the Linkedin information {information} about a person from I want you to create:
    1. a short summary
    2. two crazy facts about then

    Use infromation from Linkedin
    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables="information",
        template=summary_template,
        partial_variables={"format_instructions":summary_parser.get_format_instructions()},
        )
    llm = ChatOpenAI(temperature=0, model_name="gpt-4.1-nano")

    chain = summary_prompt_template | llm | summary_parser

   

    res:Summary = chain.invoke(input={"information":linkedin_data})
   
    return res, linkedin_data.get("photoUrl")     





if __name__ == '__main__':
    load_dotenv()

    print("starting --------------------------------")

    ice_breaker_with(name="Sanjeet kumar Java Team Lead at Central Government")
    

    
    
