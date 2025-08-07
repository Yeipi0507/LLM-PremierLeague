#!/usr/bin/env python3
"""
Quick Performance Test - LLM Premier League (Light Version)
Test rápido y económico para comparar LOCAL vs CLAUDE AI
"""

import requests
import json
import time
from datetime import datetime
import statistics

API_BASE_URL = "http://localhost:8080/api"

class QuickTester:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'local_mode': {},
            'claude_mode': {}
        }
    
    def toggle_ai_mode(self, enable: bool) -> bool:
        """Cambiar modo AI"""
        try:
            response = requests.post(f"{API_BASE_URL}/toggle-ai", 
                                   json={"use_claude_ai": enable}, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def test_endpoint(self, endpoint, payload=None, count=3):
        """Test detallado de un endpoint con métricas precisas"""
        times = []
        success = 0
        errors = []
        
        print(f"    🔍 Ejecutando {count} requests...")
        start_batch = time.time()
        
        for i in range(count):
            start = time.time()
            try:
                if payload:
                    response = requests.post(f"{API_BASE_URL}/{endpoint}", 
                                           json=payload, timeout=15)
                else:
                    response = requests.get(f"{API_BASE_URL}/{endpoint}", timeout=15)
                
                response_time = time.time() - start
                
                if response.status_code == 200:
                    success += 1
                    times.append(response_time)
                    response_size = len(response.content)
                    print(f"      {i+1}/{count}: ✅ {response_time:.3f}s ({response_size} bytes)")
                else:
                    errors.append(f"HTTP {response.status_code}")
                    print(f"      {i+1}/{count}: ❌ HTTP {response.status_code}")
                    
            except Exception as e:
                error_msg = str(e)[:50]
                errors.append(error_msg)
                print(f"      {i+1}/{count}: ❌ {error_msg}")
            
            time.sleep(0.3)  # Pausa más corta
        
        batch_time = time.time() - start_batch
        
        # Calcular estadísticas detalladas
        result = {
            'avg_time': statistics.mean(times) if times else 999,
            'min_time': min(times) if times else 0,
            'max_time': max(times) if times else 0,
            'success_rate': success / count,
            'total_tests': count,
            'successful_tests': success,
            'failed_tests': count - success,
            'batch_duration': batch_time,
            'throughput': count / batch_time,
            'errors': errors
        }
        
        # Mostrar resumen del endpoint
        print(f"    📊 Resumen: {success}/{count} exitosos, promedio {result['avg_time']:.3f}s")
        
        return result
    
    def run_quick_test(self):
        """Test detallado de 8 minutos máximo con comparaciones precisas"""
        print("🚀 DETAILED QUICK TEST - LLM Premier League")
        print("=" * 65)
        print("⏱️  Duración estimada: 6-8 minutos")
        print("💰 Costo: ~12 requests totales (6 por modo)")
        
        # Test endpoints importantes (solo los críticos)
        tests = [
            ('health', 'Health Check', None),
            ('predict', 'Prediction', {'home_team': 'Arsenal', 'away_team': 'Chelsea'}),
            ('chat', 'Chat', {'message': '¿Quién ganará la Premier League?'})
        ]
        
        # Test LOCAL mode (AI OFF)
        print(f"\n🏠 TESTING LOCAL MODE (AI OFF)")
        print("=" * 45)
        start_local = time.time()
        
        if self.toggle_ai_mode(False):
            print("✅ Modo LOCAL activado")
            time.sleep(1)
            self.results['local_mode'] = {}
            
            for endpoint, name, payload in tests:
                print(f"\n  📊 {name} Test:")
                self.results['local_mode'][endpoint] = self.test_endpoint(endpoint, payload, 2)
        else:
            print("❌ Error activando modo LOCAL")
            
        local_duration = time.time() - start_local
        print(f"\n⏱️  Tiempo total LOCAL: {local_duration:.2f}s")
        
        time.sleep(2)  # Pausa entre modos
        
        # Test CLAUDE AI mode (AI ON)
        print(f"\n🤖 TESTING CLAUDE AI MODE (AI ON)")
        print("=" * 45)
        start_claude = time.time()
        
        if self.toggle_ai_mode(True):
            print("✅ Modo CLAUDE AI activado")
            time.sleep(1)
            self.results['claude_mode'] = {}
            
            for endpoint, name, payload in tests:
                print(f"\n  📊 {name} Test:")
                self.results['claude_mode'][endpoint] = self.test_endpoint(endpoint, payload, 2)
        else:
            print("❌ Error activando modo CLAUDE AI")
            
        claude_duration = time.time() - start_claude
        print(f"\n⏱️  Tiempo total CLAUDE AI: {claude_duration:.2f}s")
        
        # Guardar duraciones totales
        self.results['mode_durations'] = {
            'local_total': local_duration,
            'claude_total': claude_duration
        }
    
    def print_summary(self):
        """Resumen detallado con comparaciones precisas"""
        print("\n" + "=" * 70)
        print("📊 DETAILED PERFORMANCE COMPARISON")
        print("=" * 70)
        
        local = self.results['local_mode']
        claude = self.results['claude_mode']
        durations = self.results.get('mode_durations', {})
        
        # Tabla comparativa detallada
        print(f"\n{'Endpoint':<12} {'LOCAL (OFF)':<20} {'CLAUDE AI (ON)':<20} {'Winner':<10}")
        print("-" * 70)
        
        endpoint_winners = {}
        
        for endpoint in local.keys():
            if endpoint in claude:
                local_time = local[endpoint]['avg_time']
                claude_time = claude[endpoint]['avg_time']
                local_success = local[endpoint]['success_rate']
                claude_success = claude[endpoint]['success_rate']
                
                # Determinar ganador por velocidad
                speed_winner = "LOCAL" if local_time < claude_time else "CLAUDE AI"
                reliability_winner = "LOCAL" if local_success > claude_success else "CLAUDE AI"
                
                endpoint_winners[endpoint] = {
                    'speed': speed_winner,
                    'reliability': reliability_winner
                }
                
                print(f"{endpoint:<12} {local_time:.3f}s ({local_success*100:3.0f}%) {claude_time:>8.3f}s ({claude_success*100:3.0f}%) {speed_winner:>10}")
        
        # Estadísticas generales
        print(f"\n📈 ESTADÍSTICAS GENERALES:")
        print("-" * 40)
        
        # Tiempos promedio
        local_avg = sum(r['avg_time'] for r in local.values()) / len(local)
        claude_avg = sum(r['avg_time'] for r in claude.values()) / len(claude)
        speed_diff = abs(local_avg - claude_avg)
        speed_improvement = ((max(local_avg, claude_avg) - min(local_avg, claude_avg)) / max(local_avg, claude_avg)) * 100
        
        print(f"⚡ Velocidad promedio:")
        print(f"   • LOCAL: {local_avg:.3f}s")
        print(f"   • CLAUDE AI: {claude_avg:.3f}s")
        print(f"   • Diferencia: {speed_diff:.3f}s ({speed_improvement:.1f}% {'LOCAL' if local_avg < claude_avg else 'CLAUDE AI'} más rápido)")
        
        # Tasas de éxito
        local_success_avg = sum(r['success_rate'] for r in local.values()) / len(local)
        claude_success_avg = sum(r['success_rate'] for r in claude.values()) / len(claude)
        
        print(f"\n✅ Confiabilidad promedio:")
        print(f"   • LOCAL: {local_success_avg*100:.1f}%")
        print(f"   • CLAUDE AI: {claude_success_avg*100:.1f}%")
        
        # Duración total de tests
        if durations:
            print(f"\n⏱️  Duración de testing:")
            print(f"   • LOCAL: {durations['local_total']:.1f}s")
            print(f"   • CLAUDE AI: {durations['claude_total']:.1f}s")
        
        # Recomendaciones detalladas
        print(f"\n🎯 RECOMENDACIONES:")
        print("-" * 30)
        
        speed_wins = sum(1 for w in endpoint_winners.values() if w['speed'] == 'LOCAL')
        
        if speed_wins >= 2:
            print("🚀 LOCAL MODE es consistentemente más rápido")
            print("   → Ideal para aplicaciones que requieren baja latencia")
            print("   → Perfecto para endpoints de alta frecuencia")
        else:
            print("🤖 CLAUDE AI competitive en velocidad")
            print("   → Acceptable para la mayoría de casos de uso")
        
        if claude_success_avg >= local_success_avg:
            print("🎯 CLAUDE AI ofrece mejor confiabilidad")
            print("   → Recomendado para casos críticos")
        
        # Recomendación final
        print(f"\n🏆 VEREDICTO FINAL:")
        if local_avg < claude_avg and local_success_avg >= claude_success_avg - 0.1:
            print("   💡 LOCAL MODE: Mejor opción general (velocidad + confiabilidad)")
        elif claude_success_avg > local_success_avg + 0.1:
            print("   💡 CLAUDE AI: Mejor para casos que requieren máxima precision")
        else:
            print("   💡 HÍBRIDO: Usar LOCAL para velocidad, CLAUDE AI para calidad")
    
    def save_results(self):
        """Guardar resultados básicos"""
        filename = f"quick_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = f"/Users/rios/Desktop/LLM-PREMIER/testing/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Resultados guardados en: {filename}")

def main():
    print("⚡ DETAILED TESTING - Análisis preciso con consumo moderado")
    print("⏱️  Duración: ~6-8 minutos")
    print("💰 Costo: ~12 requests (6 LOCAL + 6 CLAUDE AI)")
    print("🎯 Comparación detallada: ON vs OFF con métricas precisas")
    print()
    
    tester = QuickTester()
    tester.run_quick_test()
    tester.print_summary()
    tester.save_results()
    
    print(f"\n🎉 Análisis detallado completado!")
    print(f"📊 Datos precisos para tomar decisiones informadas")
    print(f"💸 Balance perfecto: detalle útil sin quebrar el wallet")

if __name__ == "__main__":
    main()
