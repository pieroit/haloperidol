from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel, Field
from datetime import datetime, date

class HaloperidolSettings(BaseModel):
    enable_double_check: bool = Field(
        default=False,
        description="If On, the Cat will double check its own reply. "
                "Will use more tokens, but reduce hallucinations even more."
    )

@plugin
def settings_model():
    return HaloperidolSettings

