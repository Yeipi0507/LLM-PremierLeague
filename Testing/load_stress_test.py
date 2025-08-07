#!/usr/bin/env python3
"""
Load & Stress Testing Suite - LLM Premier League
Evalúa el rendimiento bajo carga y stress del sistema
"""

import requests
import json
import time
import threading
from datetime import datetime
from typing import Dict, List
import statistics
import concurrent.futures
from queue import Queue

API_BASE_URL = "http://localhost:8080/api"

class LoadTester:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'load_test_results': {},
            'stress_test_results': {},
            'concurrent_test_results': {}
        }
        
        self.test_scenarios = {
            'light_load': {'users': 5, 'requests_per_user': 10, 'delay': 0.5},
            'medium_load': {'users': 10, 'requests_per_user': 20, 'delay': 0.2},
            'heavy_load': {'users': 20, 'requests_per_user': 15, 'delay': 0.1},
            'stress_test': {'users': 50, 'requests_per_user': 5, 'delay': 0.05}
        }
        
        self.test_endpoints = [
            {'name': 'health', 'method': 'GET', 'path': '/health', 'payload': None},
            {'name': 'predict_simple', 'method': 'POST', 'path': '/predict', 
             'payload': {'home_team': 'Arsenal', 'away_team': 'Chelsea'}},
            {'name': 'analyze_team', 'method': 'POST', 'path': '/analyze',
             'payload': {'team': 'Liverpool'}},
            {'name': 'chat_simple', 'method': 'POST', 'path': '/chat',
             'payload': {'message': '¿Quién ganará la Premier League?'}}
        ]
    
    def toggle_ai_mode(self, enable: bool) -> bool:
        """Cambiar modo AI"""
        try:
            response = requests.post(f"{API_BASE_URL}/toggle-ai",
                                   json={"use_claude_ai": enable}, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def make_request(self, endpoint: Dict, timeout: int = 30) -> Dict:
        """Hacer una petición a un endpoint"""
        start_time = time.time()
        
        try:
            if endpoint['method'] == 'GET':
                response = requests.get(f"{API_BASE_URL}{endpoint['path']}", timeout=timeout)
            else:
                response = requests.post(f"{API_BASE_URL}{endpoint['path']}", 
                                       json=endpoint['payload'], timeout=timeout)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response_time': response_time,
                'response_size': len(response.content),
                'error': None
            }
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'status_code': 0,
                'response_time': timeout,
                'response_size': 0,
                'error': 'timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'status_code': 0,
                'response_time': time.time() - start_time,
                'response_size': 0,
                'error': str(e)
            }
    
    def user_simulation(self, user_id: int, scenario: Dict, endpoint: Dict, results_queue: Queue):
        """Simular las peticiones de un usuario"""
        user_results = []
        
        for request_num in range(scenario['requests_per_user']):
            result = self.make_request(endpoint)
            result['user_id'] = user_id
            result['request_num'] = request_num
            result['timestamp'] = time.time()
            
            user_results.append(result)
            results_queue.put(result)
            
            # Delay entre peticiones
            if scenario['delay'] > 0:
                time.sleep(scenario['delay'])
        
        return user_results
    
    def run_load_test(self, scenario_name: str, endpoint: Dict, mode: str) -> Dict:
        """Ejecutar test de carga"""
        scenario = self.test_scenarios[scenario_name]
        print(f"🔄 Load test: {scenario_name} on {endpoint['name']} ({mode} mode)")
        print(f"   👥 Users: {scenario['users']}, Requests/user: {scenario['requests_per_user']}")
        
        results_queue = Queue()
        start_time = time.time()
        
        # Ejecutar usuarios concurrentemente
        with concurrent.futures.ThreadPoolExecutor(max_workers=scenario['users']) as executor:
            futures = []
            
            for user_id in range(scenario['users']):
                future = executor.submit(
                    self.user_simulation, user_id, scenario, endpoint, results_queue
                )
                futures.append(future)
            
            # Esperar a que terminen todos
            concurrent.futures.wait(futures)
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        # Recopilar resultados
        all_results = []
        while not results_queue.empty():
            all_results.append(results_queue.get())
        
        # Calcular estadísticas
        success_count = sum(1 for r in all_results if r['success'])
        response_times = [r['response_time'] for r in all_results]
        
        stats = {
            'total_requests': len(all_results),
            'successful_requests': success_count,
            'failed_requests': len(all_results) - success_count,
            'success_rate': success_count / len(all_results) if all_results else 0,
            'total_duration': total_duration,
            'requests_per_second': len(all_results) / total_duration,
            'avg_response_time': statistics.mean(response_times) if response_times else 0,
            'min_response_time': min(response_times) if response_times else 0,
            'max_response_time': max(response_times) if response_times else 0,
            'median_response_time': statistics.median(response_times) if response_times else 0,
            'percentile_95': statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0,
            'errors': [r for r in all_results if not r['success']]
        }
        
        print(f"   ✅ Completed: {stats['success_rate']*100:.1f}% success, {stats['requests_per_second']:.1f} RPS")
        return stats
    
    def run_concurrent_endpoint_test(self, mode: str) -> Dict:
        """Test de múltiples endpoints simultáneamente"""
        print(f"🚀 Concurrent endpoint test ({mode} mode)")
        
        results_queue = Queue()
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.test_endpoints) * 3) as executor:
            futures = []
            
            # Lanzar 3 peticiones de cada endpoint simultáneamente
            for endpoint in self.test_endpoints:
                for i in range(3):
                    future = executor.submit(self.make_request, endpoint, 60)  # Timeout más alto
                    futures.append((future, endpoint['name'], i))
            
            # Recopilar resultados
            endpoint_results = {}
            for future, endpoint_name, request_num in futures:
                try:
                    result = future.result(timeout=70)
                    result['endpoint'] = endpoint_name
                    result['request_num'] = request_num
                    
                    if endpoint_name not in endpoint_results:
                        endpoint_results[endpoint_name] = []
                    endpoint_results[endpoint_name].append(result)
                    
                except Exception as e:
                    print(f"   ❌ Error in {endpoint_name}: {e}")
        
        total_duration = time.time() - start_time
        
        # Calcular estadísticas por endpoint
        summary = {}
        for endpoint_name, results in endpoint_results.items():
            success_count = sum(1 for r in results if r['success'])
            response_times = [r['response_time'] for r in results if r['success']]
            
            summary[endpoint_name] = {
                'requests': len(results),
                'success_rate': success_count / len(results) if results else 0,
                'avg_response_time': statistics.mean(response_times) if response_times else 0,
                'max_response_time': max(response_times) if response_times else 0
            }
        
        summary['total_duration'] = total_duration
        summary['total_requests'] = sum(len(results) for results in endpoint_results.values())
        
        print(f"   ✅ Completed in {total_duration:.1f}s")
        return summary
    
    def run_stress_escalation_test(self, endpoint: Dict, mode: str) -> Dict:
        """Test de stress con escalamiento progresivo"""
        print(f"⚡ Stress escalation test on {endpoint['name']} ({mode} mode)")
        
        escalation_results = {}
        user_counts = [5, 10, 20, 30, 40, 50]
        
        for user_count in user_counts:
            print(f"   📈 Testing with {user_count} concurrent users")
            
            scenario = {'users': user_count, 'requests_per_user': 3, 'delay': 0.1}
            
            results_queue = Queue()
            start_time = time.time()
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=user_count) as executor:
                futures = [
                    executor.submit(self.user_simulation, i, scenario, endpoint, results_queue)
                    for i in range(user_count)
                ]
                concurrent.futures.wait(futures, timeout=120)
            
            # Recopilar resultados
            all_results = []
            while not results_queue.empty():
                all_results.append(results_queue.get())
            
            success_count = sum(1 for r in all_results if r['success'])
            response_times = [r['response_time'] for r in all_results if r['success']]
            
            escalation_results[user_count] = {
                'success_rate': success_count / len(all_results) if all_results else 0,
                'avg_response_time': statistics.mean(response_times) if response_times else 0,
                'requests_per_second': len(all_results) / (time.time() - start_time),
                'failed_requests': len(all_results) - success_count
            }
            
            print(f"      Success: {escalation_results[user_count]['success_rate']*100:.1f}%")
            
            # Si la tasa de éxito cae mucho, detener la escalada
            if escalation_results[user_count]['success_rate'] < 0.5:
                print(f"   🔴 Breaking point reached at {user_count} users")
                break
                
            time.sleep(2)  # Pausa entre escalaciones
        
        return escalation_results
    
    def run_all_tests(self):
        """Ejecutar toda la suite de tests"""
        print("⚡ LLM PREMIER LEAGUE - LOAD & STRESS TESTING SUITE")
        print("=" * 70)
        
        for ai_mode in [False, True]:
            mode_name = "LOCAL" if not ai_mode else "CLAUDE AI"
            print(f"\n📊 TESTING {mode_name} MODE")
            print("-" * 50)
            
            if not self.toggle_ai_mode(ai_mode):
                print(f"❌ Failed to switch to {mode_name} mode")
                continue
                
            time.sleep(2)  # Pausa después del cambio
            
            mode_results = {}
            
            # 1. Load tests básicos
            print("\n🔄 Load Tests:")
            mode_results['load_tests'] = {}
            
            for scenario_name in ['light_load', 'medium_load', 'heavy_load']:
                # Test con endpoint de predicción (más pesado)
                predict_endpoint = next(e for e in self.test_endpoints if e['name'] == 'predict_simple')
                mode_results['load_tests'][scenario_name] = self.run_load_test(
                    scenario_name, predict_endpoint, mode_name
                )
                time.sleep(1)
            
            # 2. Test concurrente de múltiples endpoints
            print("\n🚀 Concurrent Endpoints Test:")
            mode_results['concurrent_endpoints'] = self.run_concurrent_endpoint_test(mode_name)
            time.sleep(2)
            
            # 3. Stress test con escalamiento
            print("\n⚡ Stress Escalation Test:")
            chat_endpoint = next(e for e in self.test_endpoints if e['name'] == 'chat_simple')
            mode_results['stress_escalation'] = self.run_stress_escalation_test(
                chat_endpoint, mode_name
            )
            
            # Guardar resultados del modo
            if ai_mode:
                self.results['claude_ai_on'] = mode_results
            else:
                self.results['claude_ai_off'] = mode_results
    
    def save_results(self) -> str:
        """Guardar resultados"""
        filename = f"load_stress_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = f"/Users/rios/Desktop/LLM-PREMIER/testing/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Resultados guardados en: {filepath}")
        return filepath
    
    def print_summary(self):
        """Imprimir resumen comparativo"""
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE CARGA Y STRESS")
        print("=" * 70)
        
        for mode_name, mode_key in [("LOCAL", "claude_ai_off"), ("CLAUDE AI", "claude_ai_on")]:
            if mode_key not in self.results:
                continue
                
            data = self.results[mode_key]
            print(f"\n📊 MODO {mode_name}:")
            
            # Resumen de load tests
            if 'load_tests' in data:
                print("   🔄 Load Tests:")
                for scenario, results in data['load_tests'].items():
                    print(f"      {scenario}: {results['success_rate']*100:.1f}% success, "
                          f"{results['requests_per_second']:.1f} RPS, "
                          f"{results['avg_response_time']:.2f}s avg")
            
            # Test concurrente
            if 'concurrent_endpoints' in data:
                concurrent = data['concurrent_endpoints']
                print(f"   🚀 Concurrent: {concurrent['total_requests']} requests in {concurrent['total_duration']:.1f}s")
            
            # Stress test
            if 'stress_escalation' in data:
                max_users = max(data['stress_escalation'].keys())
                max_stats = data['stress_escalation'][max_users]
                print(f"   ⚡ Stress: Max {max_users} users, {max_stats['success_rate']*100:.1f}% success")

def main():
    tester = LoadTester()
    tester.run_all_tests()
    tester.print_summary()
    results_file = tester.save_results()
    return results_file

if __name__ == "__main__":
    main()
