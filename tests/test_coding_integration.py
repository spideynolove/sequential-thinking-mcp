#!/usr/bin/env python3

import pytest
import json
import time
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import the classes we need to test
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import (
    SequentialThinkingEngine, CodingWorkflowEngine, PackageDiscoveryEngine,
    ArchitectureDecisionTracker, CodingPatternDetector, CodeReinventionDetector,
    CrossSystemIntegration, PackageInfo, ArchitectureDecision
)

class TestPackageDiscoveryEngine:
    """Test suite for PackageDiscoveryEngine component."""
    
    def setup_method(self):
        self.engine = PackageDiscoveryEngine()
    
    def test_relevance_calculation(self):
        """Test relevance scoring algorithm."""
        # Perfect match
        assert self.engine._calculate_relevance("http requests", ["http", "requests"]) == 1.0
        
        # Partial match
        assert self.engine._calculate_relevance("web framework", ["web"]) == 0.5
        
        # No match
        assert self.engine._calculate_relevance("unrelated content", ["database"]) == 0.0
        
        # Empty keywords
        assert self.engine._calculate_relevance("any content", []) == 0.0
    
    def test_package_ranking(self):
        """Test package ranking prioritizes installed packages."""
        packages = [
            PackageInfo("requests", "2.31.0", "HTTP library", False, 0.8),
            PackageInfo("urllib3", "2.0.0", "HTTP library", True, 0.7)
        ]
        
        ranked = self.engine._rank_packages(packages, "http client")
        
        # Installed package should rank higher despite lower relevance
        assert ranked[0].name == "urllib3"
        assert ranked[0].installed == True
    
    @patch('subprocess.run')
    def test_search_installed_packages(self, mock_subprocess):
        """Test searching installed packages via pip."""
        # Mock pip list output
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps([
            {"name": "requests", "version": "2.31.0"},
            {"name": "pandas", "version": "2.0.0"}
        ])
        mock_subprocess.return_value = mock_result
        
        packages = self.engine._search_installed_packages("data analysis")
        
        # Should find pandas for data analysis task
        pandas_packages = [p for p in packages if p.name == "pandas"]
        assert len(pandas_packages) > 0
        assert pandas_packages[0].installed == True
    
    @patch('subprocess.run')
    def test_search_installed_packages_error_handling(self, mock_subprocess):
        """Test graceful handling of pip command errors."""
        # Mock pip command failure
        mock_subprocess.side_effect = Exception("Command failed")
        
        packages = self.engine._search_installed_packages("any task")
        
        # Should return empty list on error
        assert packages == []
    
    def test_search_pypi_common_packages(self):
        """Test PyPI search returns relevant common packages."""
        packages = self.engine._search_pypi("web framework")
        
        # Should find web frameworks
        framework_names = [p.name for p in packages]
        assert "flask" in framework_names or "django" in framework_names
        
        # All packages should have descriptions
        for package in packages:
            assert package.description != ""
            assert package.version == "latest"
            assert package.installed == False
    
    def test_discover_packages_caching(self):
        """Test package discovery caching functionality."""
        task = "test caching"
        
        # First call
        result1 = self.engine.discover_packages(task)
        
        # Second call should use cache
        result2 = self.engine.discover_packages(task)
        
        assert result1 == result2
        assert f"{task}:python" in self.engine.package_cache

class TestArchitectureDecisionTracker:
    """Test suite for ArchitectureDecisionTracker component."""
    
    def setup_method(self):
        self.tracker = ArchitectureDecisionTracker()
    
    def test_record_decision(self):
        """Test recording architecture decisions."""
        decision_id = self.tracker.record_decision(
            title="Test Decision",
            context="Test context",
            options_considered=["Option A", "Option B"],
            chosen_option="Option A",
            rationale="Better performance",
            consequences="Higher complexity",
            package_dependencies=["requests"],
            thinking_session_id="test_session"
        )
        
        assert decision_id in self.tracker.decisions
        decision = self.tracker.decisions[decision_id]
        assert decision.title == "Test Decision"
        assert decision.chosen_option == "Option A"
        assert "requests" in decision.package_dependencies
    
    def test_query_similar_decisions(self):
        """Test querying similar architecture decisions."""
        # Record some test decisions
        self.tracker.record_decision(
            "Database Selection", "Need persistent storage",
            ["PostgreSQL", "MongoDB"], "PostgreSQL",
            "ACID compliance", "Complex setup",
            ["psycopg2"], "session1"
        )
        
        self.tracker.record_decision(
            "Cache Selection", "Need fast data access",
            ["Redis", "Memcached"], "Redis",
            "Rich data types", "Memory usage",
            ["redis"], "session2"
        )
        
        # Query for database decisions
        db_decisions = self.tracker.query_similar_decisions(technology="database")
        assert len(db_decisions) >= 1
        assert any("Database" in d.title for d in db_decisions)
        
        # Query for Redis decisions
        redis_decisions = self.tracker.query_similar_decisions(package="redis")
        assert len(redis_decisions) >= 1

class TestCodingPatternDetector:
    """Test suite for CodingPatternDetector component."""
    
    def setup_method(self):
        self.detector = CodingPatternDetector()
    
    def test_detect_package_needed_pattern(self):
        """Test detection of package need patterns."""
        content = "Need to import requests library for HTTP calls"
        patterns = self.detector.detect_patterns(content)
        
        package_patterns = [p for p in patterns if p.pattern == "package_needed"]
        assert len(package_patterns) > 0
        assert package_patterns[0].confidence >= 0.7
    
    def test_detect_api_exploration_pattern(self):
        """Test detection of API exploration patterns."""
        content = "Exploring the REST API endpoints and methods"
        patterns = self.detector.detect_patterns(content)
        
        api_patterns = [p for p in patterns if p.pattern == "api_exploration"]
        assert len(api_patterns) > 0
    
    def test_detect_architecture_decision_pattern(self):
        """Test detection of architecture decision patterns."""
        content = "Need to choose between FastAPI and Django framework"
        patterns = self.detector.detect_patterns(content)
        
        decision_patterns = [p for p in patterns if p.pattern == "architecture_decision"]
        assert len(decision_patterns) > 0

class TestCodeReinventionDetector:
    """Test suite for CodeReinventionDetector component."""
    
    def setup_method(self):
        self.detector = CodeReinventionDetector()
    
    def test_detect_http_reinvention(self):
        """Test detection of HTTP request reinvention."""
        code = """
        def custom_http_get(url):
            import socket
            # Custom HTTP implementation
            return response
        """
        
        result = self.detector.detect_reinvention(code, [], 0.7)
        
        assert result['is_potential_reinvention'] == True
        assert result['confidence_score'] >= 0.7
        assert any(p['functionality'] == 'http_requests' for p in result['detected_patterns'])
    
    def test_detect_data_processing_reinvention(self):
        """Test detection of data processing reinvention."""
        code = """
        def parse_csv_manually(filename):
            # Custom CSV parsing logic
            return parsed_data
        """
        
        result = self.detector.detect_reinvention(code, [], 0.8)
        
        assert result['is_potential_reinvention'] == True
        processing_patterns = [p for p in result['detected_patterns'] 
                             if p['functionality'] == 'data_processing']
        assert len(processing_patterns) > 0
    
    def test_no_reinvention_detected(self):
        """Test case where no reinvention is detected."""
        code = """
        def business_specific_calculation(data):
            # Domain-specific business logic
            return result
        """
        
        result = self.detector.detect_reinvention(code, [], 0.8)
        
        assert result['is_potential_reinvention'] == False
        assert result['confidence_score'] < 0.8

class TestCodingWorkflowEngine:
    """Test suite for CodingWorkflowEngine integration."""
    
    def setup_method(self):
        self.thinking_engine = SequentialThinkingEngine()
        self.coding_engine = CodingWorkflowEngine(self.thinking_engine)
    
    def test_start_coding_session(self):
        """Test starting a coding session."""
        session_id = self.coding_engine.start_coding_session(
            problem="Build web API",
            success_criteria="RESTful endpoints",
            constraints=["Use Python", "Docker deployment"]
        )
        
        session = self.thinking_engine.session_manager.get_session(session_id)
        assert session is not None
        assert session.coding_session == True
        assert "Use Python" in session.constraints
    
    def test_explore_packages_integration(self):
        """Test package exploration integration with thinking session."""
        # Start session
        session_id = self.coding_engine.start_coding_session(
            "Build HTTP client", "Fast and reliable"
        )
        
        # Explore packages
        packages = self.coding_engine.explore_packages(
            "HTTP client", "python", session_id
        )
        
        # Verify packages stored in session
        session = self.thinking_engine.session_manager.get_session(session_id)
        assert len(session.package_registry) > 0
        
        # Verify relevant packages found
        package_names = [p.name for p in packages]
        assert any("request" in name.lower() for name in package_names)
    
    def test_record_architecture_decision_integration(self):
        """Test architecture decision recording integration."""
        # Start session
        session_id = self.coding_engine.start_coding_session(
            "Database selection", "ACID compliance required"
        )
        
        # Record decision
        decision_id = self.coding_engine.record_architecture_decision(
            title="Database Choice",
            context="Need ACID compliance",
            options_considered=["PostgreSQL", "MySQL"],
            chosen_option="PostgreSQL",
            rationale="Better JSON support",
            consequences="PostgreSQL expertise required",
            package_dependencies=["psycopg2"],
            thinking_session_id=session_id
        )
        
        # Verify decision stored
        session = self.thinking_engine.session_manager.get_session(session_id)
        assert decision_id in session.architecture_decisions
        
        decision = session.architecture_decisions[decision_id]
        assert decision.title == "Database Choice"
        assert "psycopg2" in decision.package_dependencies

class TestCrossSystemIntegration:
    """Test suite for CrossSystemIntegration component."""
    
    def setup_method(self):
        self.thinking_engine = SequentialThinkingEngine()
        self.integration = CrossSystemIntegration(self.thinking_engine)
    
    def test_get_package_context(self):
        """Test getting package context for external systems."""
        # Start coding session
        session_id = self.thinking_engine.start_session(
            "Test problem", "Test criteria", [], coding_session=True
        )
        
        # Add some package data
        session = self.thinking_engine.session_manager.get_session(session_id)
        session.package_registry["requests"] = PackageInfo(
            "requests", "2.31.0", "HTTP library", True, 0.9
        )
        
        # Get context
        context = self.integration.get_package_context(session_id)
        
        assert "packages" in context
        assert "requests" in context["packages"]
        assert context["coding_session"] == True
    
    def test_set_external_package_context(self):
        """Test setting external package context."""
        # Start session
        session_id = self.thinking_engine.start_session(
            "Test problem", "Test criteria", [], coding_session=True
        )
        
        # Set external context
        external_context = {
            "packages": {
                "pandas": {
                    "name": "pandas",
                    "version": "2.0.0",
                    "description": "Data analysis library",
                    "installed": False,
                    "relevance_score": 0.8,
                    "integration_examples": [],
                    "api_methods": []
                }
            }
        }
        
        self.integration.set_external_package_context(session_id, external_context)
        
        # Verify integration
        session = self.thinking_engine.session_manager.get_session(session_id)
        assert "pandas" in session.package_registry
        assert session.package_registry["pandas"].version == "2.0.0"

class TestPerformanceValidation:
    """Test suite for performance validation."""
    
    def setup_method(self):
        self.thinking_engine = SequentialThinkingEngine()
    
    def test_coding_session_performance(self):
        """Test coding session creation performance."""
        # Baseline: regular thinking session
        start_time = time.time()
        basic_session = self.thinking_engine.start_session(
            "Basic problem", "Basic criteria", []
        )
        baseline_time = time.time() - start_time
        
        # Coding session
        start_time = time.time()
        coding_session = self.thinking_engine.coding_workflow.start_coding_session(
            "Coding problem", "Coding criteria", []
        )
        coding_time = time.time() - start_time
        
        # Performance regression check (max 3x overhead)
        assert coding_time < baseline_time * 3
        
        # Cleanup
        self.thinking_engine.session_manager.cleanup_session(basic_session)
        self.thinking_engine.session_manager.cleanup_session(coding_session)
    
    def test_package_discovery_performance(self):
        """Test package discovery performance."""
        start_time = time.time()
        
        packages = self.thinking_engine.coding_workflow.explore_packages(
            "web framework", "python"
        )
        
        discovery_time = time.time() - start_time
        
        # Should complete within reasonable time (5 seconds)
        assert discovery_time < 5.0
        assert len(packages) > 0
    
    def test_memory_usage_reasonable(self):
        """Test memory usage stays within reasonable bounds."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create multiple coding sessions
        sessions = []
        for i in range(5):
            session_id = self.thinking_engine.coding_workflow.start_coding_session(
                f"Problem {i}", f"Criteria {i}", []
            )
            sessions.append(session_id)
            
            # Add some thoughts and packages
            packages = self.thinking_engine.coding_workflow.explore_packages(
                "test framework", "python", session_id
            )
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB for 5 sessions)
        assert memory_increase < 100
        
        # Cleanup
        for session_id in sessions:
            self.thinking_engine.session_manager.cleanup_session(session_id)

class TestIntegrationWorkflows:
    """Integration tests for complete coding workflows."""
    
    def setup_method(self):
        self.thinking_engine = SequentialThinkingEngine()
    
    @pytest.mark.asyncio
    async def test_complete_coding_workflow(self):
        """Test complete end-to-end coding workflow."""
        # 1. Start coding session
        session_id = self.thinking_engine.coding_workflow.start_coding_session(
            problem="Build web scraper for e-commerce data",
            success_criteria="Extract product prices efficiently",
            package_exploration_required=True
        )
        
        assert session_id is not None
        session = self.thinking_engine.session_manager.get_session(session_id)
        assert session.coding_session == True
        
        # 2. Explore packages
        packages = self.thinking_engine.coding_workflow.explore_packages(
            "web scraping", "python", session_id
        )
        
        assert len(packages) > 0
        package_names = [p.name for p in packages]
        assert any("request" in name.lower() for name in package_names)
        
        # 3. Add coding thought
        self.thinking_engine.current_session = session_id
        thought_id = await self.thinking_engine.add_thought(
            "Should use requests for HTTP and BeautifulSoup for parsing",
            coding_context=True,
            packages_explored=packages[:3]
        )
        
        thought = self.thinking_engine.thoughts[thought_id]
        assert thought.coding_context == True
        assert len(thought.packages_explored) == 3
        
        # 4. Record architecture decision
        decision_id = self.thinking_engine.coding_workflow.record_architecture_decision(
            title="Web Scraping Technology Stack",
            context="Need to scrape product data from multiple sites",
            options_considered=["requests+bs4", "scrapy", "selenium"],
            chosen_option="requests + beautifulsoup4",
            rationale="Simple, lightweight, sufficient for basic scraping",
            consequences="May need upgrade for JavaScript-heavy sites",
            package_dependencies=["requests", "beautifulsoup4"],
            thinking_session_id=session_id
        )
        
        assert decision_id in session.architecture_decisions
        
        # 5. Check for code reinvention
        reinvention_result = self.thinking_engine.coding_workflow.detect_code_reinvention(
            "def custom_http_get(url): # custom implementation",
            ["requests"]
        )
        
        assert reinvention_result['is_potential_reinvention'] == True
        
        # 6. Get cross-system context
        cross_system = CrossSystemIntegration(self.thinking_engine)
        context = cross_system.get_package_context(session_id)
        
        assert "packages" in context
        assert len(context["packages"]) > 0
        assert "architecture_decisions" in context
        assert decision_id in [str(k) for k in context["architecture_decisions"].keys()]
    
    def test_error_recovery_workflow(self):
        """Test graceful error handling in workflows."""
        # Test with invalid session
        packages = self.thinking_engine.coding_workflow.explore_packages(
            "test task", "python", "invalid_session_id"
        )
        # Should not crash, may return empty list
        assert isinstance(packages, list)
        
        # Test with empty task description
        packages = self.thinking_engine.coding_workflow.explore_packages(
            "", "python"
        )
        assert isinstance(packages, list)
        
        # Test reinvention detection with empty code
        result = self.thinking_engine.coding_workflow.detect_code_reinvention("", [])
        assert "is_potential_reinvention" in result
        assert result["is_potential_reinvention"] == False

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "--tb=short"])