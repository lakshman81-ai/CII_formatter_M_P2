import pydantic

class OptimizationSettings(pydantic.BaseModel):
    max_iterations: int = 100
    learning_rate: float = 0.1
    target_diff_bytes: int = 0
