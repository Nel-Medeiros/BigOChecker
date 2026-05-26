from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from analyzer import analyze
from analyzer.models import FunctionResult
from analyzer.parser import PythonSyntaxError

app = FastAPI(title="BigO Checker")


class AnalyzeRequest(BaseModel):
    source: str = Field(min_length=1, max_length=50_000)

    @field_validator("source")
    @classmethod
    def source_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("source must not be blank")
        return v


@app.post("/analyze", response_model=list[FunctionResult])
def analyze_endpoint(request: AnalyzeRequest) -> list[FunctionResult]:
    try:
        return analyze(request.source)
    except PythonSyntaxError as e:
        raise HTTPException(
            status_code=400,
            detail={"message": e.message, "line": e.line},
        )


app.mount("/", StaticFiles(directory="static", html=True), name="static")
