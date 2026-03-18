from parser import CIIParser, ParserSettings
from serializer import CIISerializer, SerializerSettings
from comparator import compare_files
from logger import get_logger
import random

logger = get_logger("optimizer")

from optimizer_settings import OptimizationSettings

class SerializationOptimizer:
    def __init__(self, original_path: str, data: dict, settings: OptimizationSettings):
        self.original_path = original_path
        self.data = data
        self.settings = settings

        with open(original_path, 'rb') as f:
            self.original_bytes = f.read()

    def optimize(self) -> dict:
        """
        Naive local search for demonstration purposes.
        Tries different format string parameters to minimize byte diff.
        """
        logger.info("[OPTIMIZE] Starting format optimization loop...")

        best_diff = len(self.original_bytes)
        best_format = "{:13.6G}"

        # Dynamic parameter space search over fixed widths, zero reps, and precisions
        param_space = []
        for width in [13]:
            for prec in [4, 5, 6, 7]:
                for type_char in ['G', 'E', 'f']:
                    param_space.append(f"{{:{width}.{prec}{type_char}}}")

        # Also test different padding or string formats if desired
        param_space.extend([
            "{:13.6g}", "{:13.5g}"
        ])

        for idx, fmt in enumerate(param_space):
            if idx >= self.settings.max_iterations:
                break
            s_settings = SerializerSettings(real_format=fmt)
            serializer = CIISerializer(s_settings)

            gen_str = serializer.serialize(self.data)
            gen_bytes = gen_str.encode('latin-1')

            diff_result = compare_files(self.original_path, gen_bytes)

            # Simple heuristic: byte length difference and diff line count
            diff_lines = diff_result.generate_diff_report().count('\n')

            logger.info(f"[OPTIMIZE] Attempted format '{fmt}' -> Diff metric: {diff_lines} lines")

            if diff_lines < best_diff:
                best_diff = diff_lines
                best_format = fmt

            if diff_result.is_exact_match:
                logger.info("[OPTIMIZE] Exact match found!")
                return {"exact_match": True, "best_format": best_format}

        logger.info(f"[OPTIMIZE] Optimization ended. Best format: {best_format} (diff metric: {best_diff})")
        return {"exact_match": False, "best_format": best_format, "min_diff": best_diff}
