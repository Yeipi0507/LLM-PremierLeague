#!/usr/bin/env python3
"""
Quality Testing Suite - LLM Premier League
Evalúa la calidad de las respuestas entre modo Claude AI vs modo Local
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple
import re

API_BASE_URL = "http://localhost:8080/api"

class QualityTester:
    def __init__(self):
        self.quality_tests = {
            'predictions': [
                {
                    'test_name': 'Liverpool vs Chelsea',
                    'payload': {'home_team': 'Liverpool', 'away_team': 'Chelsea'},
                    'quality_metrics': [
                        'has_probabilities',
                        'has_reasoning', 
                        'has_insights',
                        'realistic_probabilities',
                        'detailed_analysis'
                    ]
                },
                {
                    'test_name': 'Arsenal vs Man City', 
                    'payload': {'home_team': 'Arsenal', 'away_team': 'Man City'},
                    'quality_metrics': [
                        'has_probabilities',
                        'has_reasoning',
                        'has_insights', 
                        'realistic_probabilities',
                        'detailed_analysis'
                    ]
                }
            ],
            'analysis': [
                {
                    'test_name': 'Arsenal Analysis',
                    'payload': {'team': 'Arsenal'},
                    'quality_metrics': [
                        'has_strengths',
                        'has_weaknesses',
                        'has_key_players',
                        'has_form_assessment',
                        'contextual_information'
                    ]
                },
                {
                    'test_name': 'Liverpool Analysis',
                    'payload': {'team': 'Liverpool'},
                    'quality_metrics': [
                        'has_strengths',
                        'has_weaknesses', 
                        'has_key_players',
                        'has_form_assessment',
                        'contextual_information'
                    ]
                }
            ],
            'chat': [
                {
                    'test_name': 'Maximum Scorer Question',
                    'payload': {'message': '¿Quién será el máximo goleador esta temporada?'},
                    'quality_metrics': [
                        'mentions_players',
                        'provides_reasoning',
                        'includes_probabilities_or_stats',
                        'contextual_analysis',
                        'comprehensive_answer'
                    ]
                },
                {
                    'test_name': 'Team Comparison',
                    'payload': {'message': '¿Quién ganaría entre Chelsea y Liverpool?'},
                    'quality_metrics': [
                        'compares_both_teams',
                        'provides_reasoning',
                        'includes_probabilities_or_stats', 
                        'mentions_specific_factors',
                        'gives_conclusion'
                    ]
                }
            ]
        }
        
        self.results = {
            'claude_ai_on': {},
            'claude_ai_off': {},
            'timestamp': datetime.now().isoformat()
        }
    
    def toggle_ai_mode(self, enable: bool) -> bool:
        """Cambiar modo AI"""
        try:
            response = requests.post(f"{API_BASE_URL}/toggle-ai", 
                                   json={"use_claude_ai": enable}, timeout=10)
            return response.status_code == 200 and response.json().get('current_mode') == enable
        except:
            return False
    
    def evaluate_prediction_quality(self, response_data: Dict) -> Dict:
        """Evaluar calidad de predicción"""
        scores = {}
        prediction = response_data.get('prediction', {})
        
        # Has probabilities
        scores['has_probabilities'] = all(
            key in prediction for key in 
            ['win_probability_home', 'win_probability_draw', 'win_probability_away']
        )
        
        # Has reasoning
        reasoning = prediction.get('reasoning', '')
        scores['has_reasoning'] = len(reasoning) > 50
        
        # Has insights 
        insights = prediction.get('key_insights', [])
        scores['has_insights'] = len(insights) >= 2
        
        # Realistic probabilities
        probs = [
            prediction.get('win_probability_home', 0),
            prediction.get('win_probability_draw', 0), 
            prediction.get('win_probability_away', 0)
        ]
        prob_sum = sum(probs)
        scores['realistic_probabilities'] = 0.95 <= prob_sum <= 1.05 and all(0 <= p <= 1 for p in probs)
        
        # Detailed analysis
        scores['detailed_analysis'] = (
            len(reasoning) > 100 and 
            len(insights) >= 3 and
            len(str(prediction)) > 300
        )
        
        return scores
    
    def evaluate_analysis_quality(self, response_data: Dict) -> Dict:
        """Evaluar calidad de análisis de equipo"""
        scores = {}
        analysis = response_data.get('analysis', {})
        
        # Has strengths
        strengths = analysis.get('strengths', [])
        scores['has_strengths'] = len(strengths) >= 2
        
        # Has weaknesses
        weaknesses = analysis.get('weaknesses', [])
        scores['has_weaknesses'] = len(weaknesses) >= 1
        
        # Has key players
        players = analysis.get('key_players', [])
        scores['has_key_players'] = len(players) >= 1
        
        # Has form assessment
        form = analysis.get('recent_form', '')
        scores['has_form_assessment'] = len(form) > 10
        
        # Contextual information
        scores['contextual_information'] = (
            'entrenador' in str(analysis).lower() or
            'manager' in str(analysis).lower() or
            '2024' in str(analysis) or 
            'temporada' in str(analysis).lower()
        )
        
        return scores
    
    def evaluate_chat_quality(self, response_data: Dict, test_case: Dict) -> Dict:
        """Evaluar calidad de respuesta de chat"""
        scores = {}
        response_text = response_data.get('response', '').lower()
        test_name = test_case['test_name']
        
        if 'maximum scorer' in test_name.lower():
            # Mentions players
            player_keywords = ['haaland', 'salah', 'kane', 'núñez', 'jesus', 'isak', 'watkins']
            scores['mentions_players'] = any(player in response_text for player in player_keywords)
            
            # Provides reasoning
            scores['provides_reasoning'] = any(word in response_text for word in 
                ['porque', 'debido', 'razón', 'factor', 'considera'])
            
            # Includes probabilities or stats
            scores['includes_probabilities_or_stats'] = (
                '%' in response_text or
                'probabilidad' in response_text or
                'goles' in response_text or
                any(str(i) in response_text for i in range(10, 100))
            )
            
        elif 'comparison' in test_name.lower():
            # Compares both teams
            scores['compares_both_teams'] = (
                'chelsea' in response_text and 'liverpool' in response_text
            )
            
            # Provides reasoning
            scores['provides_reasoning'] = any(word in response_text for word in
                ['porque', 'debido', 'razón', 'factor', 'considera'])
            
            # Includes probabilities or stats
            scores['includes_probabilities_or_stats'] = (
                '%' in response_text or 'probabilidad' in response_text
            )
            
            # Mentions specific factors
            scores['mentions_specific_factors'] = any(word in response_text for word in
                ['forma', 'entrenador', 'plantilla', 'lesiones', 'histórico', 'casa'])
            
            # Gives conclusion
            scores['gives_conclusion'] = any(word in response_text for word in
                ['concluyo', 'considero', 'creo', 'favorito', 'victoria'])
        
        # Common metrics
        scores['contextual_analysis'] = '2024' in response_text or 'temporada' in response_text
        scores['comprehensive_answer'] = len(response_data.get('response', '')) > 200
        
        return scores
    
    def test_endpoint_quality(self, endpoint: str, test_cases: List[Dict], mode: str) -> Dict:
        """Test calidad de un endpoint específico"""
        print(f"🔍 Testing {endpoint} quality in {mode} mode...")
        results = {}
        
        for test_case in test_cases:
            test_name = test_case['test_name']
            payload = test_case['payload']
            
            print(f"  📋 {test_name}")
            
            try:
                response = requests.post(f"{API_BASE_URL}/{endpoint}", 
                                       json=payload, timeout=30)
                
                if response.status_code == 200:
                    response_data = response.json()
                    
                    # Evaluar según el tipo de endpoint
                    if endpoint == 'predict':
                        scores = self.evaluate_prediction_quality(response_data)
                    elif endpoint == 'analyze':
                        scores = self.evaluate_analysis_quality(response_data)
                    elif endpoint == 'chat':
                        scores = self.evaluate_chat_quality(response_data, test_case)
                    
                    # Calcular score total
                    total_score = sum(scores.values()) / len(scores) if scores else 0
                    
                    results[test_name] = {
                        'scores': scores,
                        'total_score': total_score,
                        'response_length': len(str(response_data)),
                        'sample_response': str(response_data)[:500] + '...' if len(str(response_data)) > 500 else str(response_data)
                    }
                    
                    print(f"    ✅ Score: {total_score:.2f} ({total_score*100:.0f}%)")
                    
                else:
                    results[test_name] = {
                        'error': f"HTTP {response.status_code}",
                        'total_score': 0
                    }
                    print(f"    ❌ Error: {response.status_code}")
                    
            except Exception as e:
                results[test_name] = {
                    'error': str(e),
                    'total_score': 0
                }
                print(f"    ❌ Exception: {e}")
            
            time.sleep(1)  # Pausa entre tests
        
        return results
    
    def run_quality_tests(self):
        """Ejecutar todos los tests de calidad"""
        print("🏆 LLM PREMIER LEAGUE - QUALITY TESTING SUITE")
        print("=" * 70)
        
        # Test modo Local (AI OFF)
        print("\n📊 TESTING LOCAL MODE (AI OFF)")
        print("-" * 50)
        
        if self.toggle_ai_mode(False):
            time.sleep(2)
            
            mode_results = {}
            mode_results['predictions'] = self.test_endpoint_quality(
                'predict', self.quality_tests['predictions'], 'LOCAL'
            )
            mode_results['analysis'] = self.test_endpoint_quality(
                'analyze', self.quality_tests['analysis'], 'LOCAL'  
            )
            mode_results['chat'] = self.test_endpoint_quality(
                'chat', self.quality_tests['chat'], 'LOCAL'
            )
            
            self.results['claude_ai_off'] = mode_results
            
        # Test modo Claude AI (AI ON)
        print("\n🤖 TESTING CLAUDE AI MODE (AI ON)")
        print("-" * 50)
        
        if self.toggle_ai_mode(True):
            time.sleep(2)
            
            mode_results = {}
            mode_results['predictions'] = self.test_endpoint_quality(
                'predict', self.quality_tests['predictions'], 'CLAUDE AI'
            )
            mode_results['analysis'] = self.test_endpoint_quality(
                'analyze', self.quality_tests['analysis'], 'CLAUDE AI'
            )
            mode_results['chat'] = self.test_endpoint_quality(
                'chat', self.quality_tests['chat'], 'CLAUDE AI'
            )
            
            self.results['claude_ai_on'] = mode_results
    
    def calculate_mode_averages(self, mode_data: Dict) -> Dict:
        """Calcular promedios por modo"""
        all_scores = []
        category_averages = {}
        
        for category, tests in mode_data.items():
            scores = [test.get('total_score', 0) for test in tests.values()]
            category_averages[category] = sum(scores) / len(scores) if scores else 0
            all_scores.extend(scores)
        
        overall_average = sum(all_scores) / len(all_scores) if all_scores else 0
        
        return {
            'overall_quality_score': overall_average,
            'category_scores': category_averages,
            'total_tests': len(all_scores)
        }
    
    def save_results(self) -> str:
        """Guardar resultados"""
        filename = f"quality_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = f"/Users/rios/Desktop/LLM-PREMIER/testing/{filename}"
        
        # Calcular promedios
        self.results['claude_ai_off']['summary'] = self.calculate_mode_averages(
            self.results['claude_ai_off']
        )
        self.results['claude_ai_on']['summary'] = self.calculate_mode_averages(
            self.results['claude_ai_on']
        )
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Resultados guardados en: {filepath}")
        return filepath
    
    def print_summary(self):
        """Imprimir resumen de resultados"""
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE CALIDAD")
        print("=" * 70)
        
        local_summary = self.results['claude_ai_off']['summary']
        ai_summary = self.results['claude_ai_on']['summary']
        
        print(f"📊 MODO LOCAL:")
        print(f"   • Score promedio: {local_summary['overall_quality_score']:.2f} ({local_summary['overall_quality_score']*100:.0f}%)")
        print(f"   • Predicciones: {local_summary['category_scores']['predictions']:.2f}")
        print(f"   • Análisis: {local_summary['category_scores']['analysis']:.2f}")
        print(f"   • Chat: {local_summary['category_scores']['chat']:.2f}")
        
        print(f"\n🤖 MODO CLAUDE AI:")
        print(f"   • Score promedio: {ai_summary['overall_quality_score']:.2f} ({ai_summary['overall_quality_score']*100:.0f}%)")
        print(f"   • Predicciones: {ai_summary['category_scores']['predictions']:.2f}")
        print(f"   • Análisis: {ai_summary['category_scores']['analysis']:.2f}")
        print(f"   • Chat: {ai_summary['category_scores']['chat']:.2f}")
        
        # Comparación
        quality_diff = ai_summary['overall_quality_score'] - local_summary['overall_quality_score']
        print(f"\n⚖️ COMPARACIÓN:")
        print(f"   • Claude AI: {quality_diff:+.2f} puntos {'mejor' if quality_diff > 0 else 'peor'}")
        print(f"   • Mejora: {quality_diff/local_summary['overall_quality_score']*100:+.1f}%" if local_summary['overall_quality_score'] > 0 else "   • No se puede calcular mejora")

def main():
    tester = QualityTester()
    tester.run_quality_tests()
    tester.print_summary()
    results_file = tester.save_results()
    return results_file

if __name__ == "__main__":
    main()
