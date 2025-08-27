from pydantic import BaseModel, Field
from typing import List, Literal

# A list of common infrastructure component types.
# This helps the LLM to categorize the extracted elements.
NodeType = Literal[
    "Zbiornik Wody",
    "Pompownia",
    "Rurociąg",
    "Zawór",
    "Zawór Bezpieczeństwa",
    "Stacja Uzdatniania Wody",
    "Osiedle",
    "Strefa Przemysłowa",
    "Inne"
]

class InfrastructureElement(BaseModel):
    """Represents a single node in the infrastructure graph."""
    id: str = Field(..., description="A short, unique identifier for the element, e.g., 'Z1', 'P1', 'R1'.")
    type: NodeType = Field(..., description="The type of the infrastructure element.")
    description: str = Field(..., description="A brief description of the element, extracted from the text.")

class Relationship(BaseModel):
    """Represents a directed connection between two nodes in the infrastructure graph."""
    source: str = Field(..., description="The ID of the source element in the relationship.")
    target: str = Field(..., description="The ID of the target element in the relationship.")
    label: str = Field(..., description="A descriptive label for the relationship, e.g., 'POŁĄCZONY_Z', 'ZASILA', 'TŁOCZY_DO'.")
    context: str = Field(..., description="The sentence or phrase from the text that justifies this relationship.")

class InfrastructureGraph(BaseModel):
    """Represents the entire extracted infrastructure graph from the text."""
    elements: List[InfrastructureElement] = Field(..., description="A list of all identified infrastructure elements.")
    relationships: List[Relationship] = Field(..., description="A list of all identified relationships between the elements.")
