#!/usr/bin/env python3
"""
Mini Quality Test - LLM Premier League (Wallet-Friendly Version)
Test básico de calidad sin quebrar el banco
"""

import requests
import json
import time
from datetime import datetime

API_BASE_URL = "http://localhost:8080/api"

class MiniQualityTester:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'local_quality': {},
            'claude_quality': {}
        }
    
    def toggle_ai_mode(self, enable: bool) -> bool:
        """Cambiar modo AI"""
        try:
            response = requests.post(f"{API_BASE_URL}/toggle-ai", 
                                   json={"use_claude_ai": enable}, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def simple_quality_check(self, response_text, test_type):
        """Check básico de calidad (sin gastar tokens)"""
        score = 0
        total = 4
        
        # Checks básicos
        if len(response_text) > 50:  # Respuesta substantiva
            score += 1
        
        if any(word in response_text.lower() for word in ['arsenal', 'chelsea', 'liverpool', 'city']):
            score += 1  # Menciona equipos
        
        if test_type == 'prediction':
            if any(word in response_text.lower() for word in ['probabilidad', '%', 'gana', 'empate']):
                score += 1
            if any(word in response_text.lower() for word in ['forma', 'casa', 'historia']):
                score += 1
        
        elif test_type == 'chat':
            if any(word in response_text.lower() for word in ['creo', 'considero', 'porque', 'debido']):
                score += 1
            if '2024' in response_text or 'temporada' in response_text.lower():
                score += 1
        
        return score / total
    
    def test_mode_quality(self, mode_name):
        """Test detallado de calidad de un modo"""
        results = {}
        start_mode = time.time()
        
        # Test 1: Predicción detallada
        print(f"  🔮 Predicción Arsenal vs Chelsea...")
        pred_start = time.time()
        try:
            response = requests.post(f"{API_BASE_URL}/predict", 
                                   json={'home_team': 'Arsenal', 'away_team': 'Chelsea'}, 
                                   timeout=25)
            pred_time = time.time() - pred_start
            
            if response.status_code == 200:
                pred_data = response.json()
                pred_text = str(pred_data)
                results['prediction'] = {
                    'quality_score': self.simple_quality_check(pred_text, 'prediction'),
                    'response_time': pred_time,
                    'response_length': len(pred_text),
                    'has_probabilities': any(word in pred_text.lower() for word in ['probability', 'probabilidad', '%']),
                    'mentions_teams': 'arsenal' in pred_text.lower() and 'chelsea' in pred_text.lower(),
                    'status': 'success'
                }
                print(f"      ✅ Score: {results['prediction']['quality_score']:.2f} ({pred_time:.2f}s)")
            else:
                results['prediction'] = {'quality_score': 0, 'status': f'error_{response.status_code}', 'response_time': pred_time}
                print(f"      ❌ Error HTTP {response.status_code} ({pred_time:.2f}s)")
        except Exception as e:
            pred_time = time.time() - pred_start
            results['prediction'] = {'quality_score': 0, 'status': 'exception', 'response_time': pred_time, 'error': str(e)[:100]}
            print(f"      ❌ Exception: {str(e)[:50]} ({pred_time:.2f}s)")
        
        time.sleep(1)
        
        # Test 2: Chat detallado
        print(f"  💬 Chat comparison question...")
        chat_start = time.time()
        try:
            response = requests.post(f"{API_BASE_URL}/chat", 
                                   json={'message': '¿Quién es mejor actualmente, Arsenal o Chelsea? Explica tu respuesta.'}, 
                                   timeout=25)
            chat_time = time.time() - chat_start
            
            if response.status_code == 200:
                chat_data = response.json()
                chat_text = chat_data.get('response', '')
                results['chat'] = {
                    'quality_score': self.simple_quality_check(chat_text, 'chat'),
                    'response_time': chat_time,
                    'response_length': len(chat_text),
                    'mentions_both_teams': 'arsenal' in chat_text.lower() and 'chelsea' in chat_text.lower(),
                    'provides_reasoning': any(word in chat_text.lower() for word in ['porque', 'debido', 'razón', 'mejor']),
                    'is_conversational': len(chat_text) > 100,
                    'status': 'success'
                }
                print(f"      ✅ Score: {results['chat']['quality_score']:.2f} ({chat_time:.2f}s)")
            else:
                results['chat'] = {'quality_score': 0, 'status': f'error_{response.status_code}', 'response_time': chat_time}
                print(f"      ❌ Error HTTP {response.status_code} ({chat_time:.2f}s)")
        except Exception as e:
            chat_time = time.time() - chat_start
            results['chat'] = {'quality_score': 0, 'status': 'exception', 'response_time': chat_time, 'error': str(e)[:100]}
            print(f"      ❌ Exception: {str(e)[:50]} ({chat_time:.2f}s)")
        
        # Calcular estadísticas del modo
        mode_time = time.time() - start_mode
        results['mode_summary'] = {
            'average_quality': (results['prediction']['quality_score'] + results['chat']['quality_score']) / 2,
            'average_response_time': (results['prediction']['response_time'] + results['chat']['response_time']) / 2,
            'total_mode_time': mode_time,
            'successful_tests': sum(1 for test in [results['prediction'], results['chat']] if test['status'] == 'success')
        }
        
        print(f"  📊 Modo {mode_name}: {results['mode_summary']['average_quality']:.2f} calidad, {results['mode_summary']['average_response_time']:.2f}s promedio")
        
        return results
    
    def run_mini_quality_test(self):
        """Test de calidad súper rápido"""
        print("🎯 MINI QUALITY TEST - LLM Premier League")
        print("=" * 55)
        print("💡 Solo 4 requests total para ahorrar tokens!")
        
        # Test LOCAL
        print("\n🏠 LOCAL MODE QUALITY:")
        if self.toggle_ai_mode(False):
            time.sleep(1)
            self.results['local_quality'] = self.test_mode_quality('LOCAL')
        
        time.sleep(2)
        
        # Test CLAUDE AI
        print("\n🤖 CLAUDE AI MODE QUALITY:")
        if self.toggle_ai_mode(True):
            time.sleep(1)
            self.results['claude_quality'] = self.test_mode_quality('CLAUDE AI')
    
    def print_summary(self):
        """Resumen detallado de calidad con comparaciones precisas"""
        print("\n" + "=" * 70)
        print("🎯 DETAILED QUALITY COMPARISON")
        print("=" * 70)
        
        local = self.results['local_quality']
        claude = self.results['claude_quality']
        
        # Comparación detallada por test
        print(f"\n{'Test':<12} {'LOCAL (OFF)':<25} {'CLAUDE AI (ON)':<25} {'Winner':<8}")
        print("-" * 75)
        
        # Predicciones
        local_pred = local.get('prediction', {})
        claude_pred = claude.get('prediction', {})
        
        local_pred_score = local_pred.get('quality_score', 0)
        claude_pred_score = claude_pred.get('quality_score', 0)
        local_pred_time = local_pred.get('response_time', 999)
        claude_pred_time = claude_pred.get('response_time', 999)
        
        pred_winner = "LOCAL" if local_pred_score >= claude_pred_score else "CLAUDE AI"
        speed_winner = "LOCAL" if local_pred_time < claude_pred_time else "CLAUDE AI"
        
        print(f"{'Prediction':<12} {local_pred_score:.2f} ({local_pred_time:.2f}s){'':<8} {claude_pred_score:.2f} ({claude_pred_time:.2f}s){'':<8} {pred_winner:<8}")
        
        # Chat
        local_chat = local.get('chat', {})
        claude_chat = claude.get('chat', {})
        
        local_chat_score = local_chat.get('quality_score', 0)
        claude_chat_score = claude_chat.get('quality_score', 0)
        local_chat_time = local_chat.get('response_time', 999)
        claude_chat_time = claude_chat.get('response_time', 999)
        
        chat_winner = "LOCAL" if local_chat_score >= claude_chat_score else "CLAUDE AI"
        
        print(f"{'Chat':<12} {local_chat_score:.2f} ({local_chat_time:.2f}s){'':<8} {claude_chat_score:.2f} ({claude_chat_time:.2f}s){'':<8} {chat_winner:<8}")
        
        # Estadísticas generales
        print(f"\n📊 ESTADÍSTICAS DETALLADAS:")
        print("-" * 45)
        
        local_summary = local.get('mode_summary', {})
        claude_summary = claude.get('mode_summary', {})
        
        local_avg_quality = local_summary.get('average_quality', 0)
        claude_avg_quality = claude_summary.get('average_quality', 0)
        local_avg_time = local_summary.get('average_response_time', 0)
        claude_avg_time = claude_summary.get('average_response_time', 0)
        
        print(f"🎯 Calidad promedio:")
        print(f"   • LOCAL: {local_avg_quality:.3f}/1.0")
        print(f"   • CLAUDE AI: {claude_avg_quality:.3f}/1.0")
        
        quality_diff = claude_avg_quality - local_avg_quality
        quality_improvement = abs(quality_diff / max(local_avg_quality, 0.001)) * 100
        
        if quality_diff > 0.05:
            print(f"   • Ventaja: CLAUDE AI es {quality_improvement:.1f}% mejor")
        elif quality_diff < -0.05:
            print(f"   • Ventaja: LOCAL es {quality_improvement:.1f}% mejor")
        else:
            print(f"   • Resultado: Calidad similar (diferencia: {abs(quality_diff):.3f})")
        
        print(f"\n⚡ Velocidad promedio:")
        print(f"   • LOCAL: {local_avg_time:.3f}s")
        print(f"   • CLAUDE AI: {claude_avg_time:.3f}s")
        
        if local_avg_time < claude_avg_time:
            speed_advantage = ((claude_avg_time - local_avg_time) / claude_avg_time) * 100
            print(f"   • LOCAL es {speed_advantage:.1f}% más rápido")
        else:
            speed_advantage = ((local_avg_time - claude_avg_time) / local_avg_time) * 100
            print(f"   • CLAUDE AI es {speed_advantage:.1f}% más rápido")
        
        # Tests exitosos
        local_success = local_summary.get('successful_tests', 0)
        claude_success = claude_summary.get('successful_tests', 0)
        print(f"\n✅ Tests exitosos:")
        print(f"   • LOCAL: {local_success}/2 ({local_success/2*100:.0f}%)")
        print(f"   • CLAUDE AI: {claude_success}/2 ({claude_success/2*100:.0f}%)")
        
        # Análisis específico
        print(f"\n� ANÁLISIS ESPECÍFICO:")
        print("-" * 35)
        
        # Predicciones
        local_has_probs = local_pred.get('has_probabilities', False)
        claude_has_probs = claude_pred.get('has_probabilities', False)
        print(f"🔮 Predicciones:")
        print(f"   • Incluye probabilidades: LOCAL={local_has_probs}, CLAUDE AI={claude_has_probs}")
        
        local_mentions = local_pred.get('mentions_teams', False)
        claude_mentions = claude_pred.get('mentions_teams', False)
        print(f"   • Menciona ambos equipos: LOCAL={local_mentions}, CLAUDE AI={claude_mentions}")
        
        # Chat
        local_reasoning = local_chat.get('provides_reasoning', False)
        claude_reasoning = claude_chat.get('provides_reasoning', False)
        print(f"💬 Chat:")
        print(f"   • Proporciona razonamiento: LOCAL={local_reasoning}, CLAUDE AI={claude_reasoning}")
        
        local_conversational = local_chat.get('is_conversational', False)
        claude_conversational = claude_chat.get('is_conversational', False)
        print(f"   • Es conversacional: LOCAL={local_conversational}, CLAUDE AI={claude_conversational}")
        
        # Recomendación final detallada
        print(f"\n🏆 RECOMENDACIÓN FINAL:")
        print("-" * 30)
        
        if claude_avg_quality > local_avg_quality + 0.1:
            print("   💡 CLAUDE AI: Significativamente superior en calidad")
            print(f"     → Mejor para casos que requieren respuestas precisas")
        elif local_avg_quality > claude_avg_quality + 0.1:
            print("   💡 LOCAL: Sorprendentemente superior en calidad")
            print(f"     → Excelente opción para la mayoría de casos")
        else:
            print("   💡 COMPETITIVO: Ambos modos ofrecen calidad similar")
        
        if local_avg_time < claude_avg_time * 0.5:
            print("   🚀 LOCAL: Significativamente más rápido")
            print(f"     → Ideal para aplicaciones en tiempo real")
        
        if claude_success > local_success:
            print("   🎯 CLAUDE AI: Más confiable")
            print(f"     → Menos probabilidad de errores")
    
    def save_results(self):
        """Guardar resultados"""
        filename = f"mini_quality_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = f"/Users/rios/Desktop/LLM-PREMIER/testing/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Guardado: {filename}")

def main():
    print("🎯 DETAILED QUALITY ANALYSIS - Análisis de calidad detallado")
    print("⏱️  Duración: ~4-5 minutos")
    print("💰 Costo: 4 requests (2 LOCAL + 2 CLAUDE AI)")
    print("🔍 Comparación detallada: Calidad ON vs OFF con métricas específicas")
    print()
    
    tester = MiniQualityTester()
    tester.run_mini_quality_test()
    tester.print_summary()
    tester.save_results()
    
    print(f"\n🎉 Análisis de calidad completado!")
    print(f"🔍 Insights detallados sobre calidad de respuestas")
    print(f"💸 Eficiente en tokens, máximo en información útil")

if __name__ == "__main__":
    main()
