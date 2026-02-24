"""Tests for Evaluator abstractions."""

import pytest
from ragmcp.evaluation.base import Evaluator


class TestEvaluatorAbstractClass:
    """Test Evaluator abstract class behavior."""

    def test_cannot_instantiate_abstract_evaluator(self):
        """Evaluator is abstract and cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Evaluator()  # type: ignore

    def test_evaluator_has_evaluate_method(self):
        """Subclass must implement evaluate() method."""
        class IncompleteEvaluator(Evaluator):
            pass  # Missing evaluate() implementation

        with pytest.raises(TypeError):
            IncompleteEvaluator()


class TestEvaluatorMethods:
    """Test Evaluator method signatures."""

    def test_evaluate_method_exists(self):
        """evaluate() method should exist on subclasses."""
        class MockEvaluator(Evaluator):
            def evaluate(
                self,
                query,
                retrieved_chunks,
                generated_answer,
                ground_truth,
            ):
                return {"precision": 0.5}

        evaluator = MockEvaluator()
        assert hasattr(evaluator, "evaluate")
        assert callable(evaluator.evaluate)

    def test_evaluate_returns_metrics_dict(self):
        """evaluate() should return a dict with string keys and float values."""
        class MockEvaluator(Evaluator):
            def evaluate(
                self,
                query,
                retrieved_chunks,
                generated_answer,
                ground_truth,
            ):
                return {
                    "precision": 0.85,
                    "recall": 0.75,
                    "f1": 0.80,
                }

        evaluator = MockEvaluator()
        metrics = evaluator.evaluate(
            query="test query",
            retrieved_chunks=["chunk1", "chunk2"],
            generated_answer="test answer",
            ground_truth="ground truth",
        )

        assert isinstance(metrics, dict)
        assert metrics["precision"] == 0.85
        assert metrics["recall"] == 0.75
        assert metrics["f1"] == 0.80

    def test_evaluate_accepts_all_parameters(self):
        """evaluate() should accept all required parameters."""
        class MockEvaluator(Evaluator):
            def evaluate(
                self,
                query,
                retrieved_chunks,
                generated_answer,
                ground_truth,
            ):
                return {
                    "query_received": query,
                    "chunks_count": len(retrieved_chunks),
                }

        evaluator = MockEvaluator()
        result = evaluator.evaluate(
            query="what is RAG?",
            retrieved_chunks=["RAG is..."],
            generated_answer="RAG stands for...",
            ground_truth="RAG means Retrieval Augmented Generation",
        )

        assert result["query_received"] == "what is RAG?"
        assert result["chunks_count"] == 1
