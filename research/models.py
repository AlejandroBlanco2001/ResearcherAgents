from pydantic import BaseModel, Field


class Intention(BaseModel):
    intent: str = Field(description="The intent of the user question.")
    research_question: str = Field(
        description="The question about the specific research."
    )
    review_question: str = Field(
        description="The question about the content of the papers."
    )


class Paper(BaseModel):
    name: str = Field(description="The name of the paper.")
    year: int = Field(description="The year of the paper.")
    authors: list[str] = Field(description="The authors of the paper.")
    abstract: str = Field(description="The abstract of the paper.")
    link: str = Field(description="The link to the paper.")
    confidence: int = Field(
        description="The confidence in the information you found from one to ten."
    )


class Resume(BaseModel):
    resume: str = Field(
        description="The resume of the best information from the papers found from the search engines."
    )
    why_is_important: str = Field(
        description="Why is important to include this information in the answer to the user question."
    )
    paper: Paper = Field(description="The paper that contains the best information.")
