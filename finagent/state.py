from pydantic import BaseModel, Field
from typing import Optional

class AgentRequest(BaseModel):
    # The only truly required field from the Frontend
    user_query: str = Field(..., description="The raw natural language query from the user")

    # All other fields should default to None. 
    # This allows the 'intent_parser' to identify missing data and fill it.
    user_name: Optional[str] = Field(None, description="Extracted name of the user")
    amount: Optional[float] = Field(None, description="Extracted transaction amount")
    
    # Behavioral data (usually passed from a DB or session, not just the query)
    avg_amount: Optional[float] = Field(None, description="Historical average amount")
    frequency: Optional[int] = Field(None, description="Current transaction frequency")
    usual_frequency: Optional[int] = Field(None, description="Historical usual frequency")
    
    # Geo-spatial data
    location: Optional[str] = Field(None, description="Current transaction location")
    usual_location: Optional[str] = Field(None, description="Historical home location")
    country: Optional[str] = Field(None, description="ISO Country code")

    # Financial health data
    credit_score: Optional[int] = Field(None, description="User credit score")
    debt: Optional[float] = Field(None, description="Current total debt")
    income: Optional[float] = Field(None, description="Annual income")
    
    # Investment data
    risk_profile: Optional[str] = Field(None, description="Calculated risk profile")
    market_ticker: Optional[str] = Field(None, description="Stock ticker symbol (e.g., NVDA)")

    class Config:
        json_schema_extra = {
            "example": {
                "user_query": "I want to buy $5000 of Apple stock from my home in Surat",
                "user_name": "Jenish Patel"
            }
        }