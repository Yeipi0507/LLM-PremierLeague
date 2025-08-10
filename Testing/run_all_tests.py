#!/usr/bin/env python3
"""
Master Test Suite Runner - LLM Premier League
Ejecuta toda la suite de tests de rendimiento de forma automatizada
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime
from pathlib import Path

class MasterTestRunner:
    def __init__(self):
        self.base_dir = "/Users/rios/Desktop/LLM-PREMIER"
        self.testing_dir = f"{self.base_dir}/testing"
        self.results_dir = f"{self.testing_dir}/results"
        
        # Crear directorio de resultados
        os.makedirs(self.results_dir, exist_ok=True)
        
        self.test_suite = {
            'performance': {
                'script': 'performance_test.py',
                'description': 'Rendimiento y Tiempos de Respuesta',
                'duration_estimate': '10-15 minutos'
            },
            'quality': {
                'script': 'quality_test.py', 
                'description': 'Calidad de Respuestas',
                'duration_estimate': '5-8 minutos'
            },
            'load_stress': {
                'script': 'load_stress_test.py',
                'description': 'Carga y Stress Testing',
                'duration_estimate': '15-20 minutos'
            }
        }
        
        self.master_results = {
            'timestamp': datetime.now().isoformat(),
            'test_results': {},
            'summary': {},
            'recommendations': []
        }
    
    def check_api_server(self) -> bool:
        """Verificar que el servidor API está corriendo"""
        import requests
        try:
            response = requests.get("http://localhost:8080/api/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def run_test_script(self, test_name: str, script_path: str) -> dict:
        """Ejecutar un script de test"""
        print(f"\n🚀 EJECUTANDO: {self.test_suite[test_name]['description']}")
        print(f"⏱️  Tiempo estimado: {self.test_suite[test_name]['duration_estimate']}")
        print("-" * 60)
        
        start_time = time.time()
        
        try:
            # Ejecutar el script
            result = subprocess.run([
                sys.executable, script_path
            ], capture_output=True, text=True, cwd=self.testing_dir, timeout=1800)  # 30 min timeout
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            if result.returncode == 0:
                print(f"✅ {test_name.upper()} completado exitosamente")
                print(f"⏱️  Tiempo real: {execution_time/60:.1f} minutos")
                
                # Buscar archivo de resultados más reciente
                result_files = list(Path(self.testing_dir).glob(f"{test_name.split('_')[0]}*results*.json"))
                latest_file = max(result_files, key=os.path.getctime) if result_files else None
                
                test_results = {}
                if latest_file:
                    with open(latest_file, 'r') as f:
                        test_results = json.load(f)
                
                return {
                    'success': True,
                    'execution_time': execution_time,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'results_file': str(latest_file) if latest_file else None,
                    'results_data': test_results
                }
            else:
                print(f"❌ {test_name.upper()} falló")
                print(f"Error: {result.stderr}")
                return {
                    'success': False,
                    'execution_time': execution_time,
                    'error': result.stderr,
                    'stdout': result.stdout
                }
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {test_name.upper()} excedió el tiempo límite")
            return {
                'success': False,
                'execution_time': 1800,
                'error': 'Timeout exceeded'
            }
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
            return {
                'success': False,
                'execution_time': time.time() - start_time,
                'error': str(e)
            }
    
    def analyze_results(self):
        """Analizar todos los resultados y generar recomendaciones"""
        print("\n🔍 ANALIZANDO RESULTADOS...")
        
        recommendations = []
        summary = {
            'total_tests_run': len([t for t in self.master_results['test_results'].values() if t['success']]),
            'failed_tests': len([t for t in self.master_results['test_results'].values() if not t['success']]),
            'total_execution_time': sum(t['execution_time'] for t in self.master_results['test_results'].values()),
            'performance_insights': {},
            'quality_insights': {},
            'load_insights': {}
        }
        
        # Analizar rendimiento
        if 'performance' in self.master_results['test_results']:
            perf_data = self.master_results['test_results']['performance'].get('results_data', {})
            if perf_data:
                # Comparar modos
                local_perf = perf_data.get('claude_ai_off', {}).get('summary', {})
                ai_perf = perf_data.get('claude_ai_on', {}).get('summary', {})
                
                if local_perf and ai_perf:
                    speed_diff = local_perf.get('avg_response_time', 0) - ai_perf.get('avg_response_time', 0)
                    success_diff = ai_perf.get('success_rate', 0) - local_perf.get('success_rate', 0)
                    
                    summary['performance_insights'] = {
                        'local_faster_by': speed_diff,
                        'ai_more_reliable_by': success_diff,
                        'local_avg_time': local_perf.get('avg_response_time', 0),
                        'ai_avg_time': ai_perf.get('avg_response_time', 0)
                    }
                    
                    if speed_diff > 0:
                        recommendations.append("🚀 Modo LOCAL es significativamente más rápido - ideal para aplicaciones que requieren baja latencia")
                    if success_diff > 0.05:
                        recommendations.append("🎯 Modo CLAUDE AI tiene mayor tasa de éxito - mejor para casos críticos")
        
        # Analizar calidad
        if 'quality' in self.master_results['test_results']:
            qual_data = self.master_results['test_results']['quality'].get('results_data', {})
            if qual_data:
                local_qual = qual_data.get('claude_ai_off', {}).get('summary', {})
                ai_qual = qual_data.get('claude_ai_on', {}).get('summary', {})
                
                if local_qual and ai_qual:
                    quality_diff = ai_qual.get('overall_quality_score', 0) - local_qual.get('overall_quality_score', 0)
                    
                    summary['quality_insights'] = {
                        'quality_improvement': quality_diff,
                        'local_quality': local_qual.get('overall_quality_score', 0),
                        'ai_quality': ai_qual.get('overall_quality_score', 0)
                    }
                    
                    if quality_diff > 0.2:
                        recommendations.append("🧠 Claude AI ofrece respuestas significativamente mejores - recomendado para experiencia premium")
                    elif quality_diff < -0.1:
                        recommendations.append("💡 Modo LOCAL sorprendentemente competitivo en calidad - excelente opción por defecto")
        
        # Analizar carga
        if 'load_stress' in self.master_results['test_results']:
            load_data = self.master_results['test_results']['load_stress'].get('results_data', {})
            if load_data:
                # Analizar límites de carga
                for mode in ['claude_ai_off', 'claude_ai_on']:
                    mode_data = load_data.get(mode, {})
                    if 'stress_escalation' in mode_data:
                        max_users = max(mode_data['stress_escalation'].keys()) if mode_data['stress_escalation'] else 0
                        mode_name = "LOCAL" if 'off' in mode else "CLAUDE AI"
                        summary['load_insights'][mode] = {'max_concurrent_users': max_users}
                        
                        if max_users >= 40:
                            recommendations.append(f"💪 Modo {mode_name} maneja alta concurrencia ({max_users}+ usuarios)")
                        elif max_users < 20:
                            recommendations.append(f"⚠️  Modo {mode_name} limitado en concurrencia (máx {max_users} usuarios)")
        
        # Recomendaciones generales
        total_time = summary['total_execution_time']
        if total_time > 1800:  # 30 minutos
            recommendations.append("⏰ Tests extensos - considera ejecutar individualmente en producción")
        
        if summary['failed_tests'] == 0:
            recommendations.append("✅ Sistema estable - todos los tests pasaron exitosamente")
        else:
            recommendations.append(f"🔧 {summary['failed_tests']} test(s) fallaron - revisar logs para optimización")
        
        self.master_results['summary'] = summary
        self.master_results['recommendations'] = recommendations
    
    def print_final_report(self):
        """Imprimir reporte final comprehensivo"""
        print("\n" + "=" * 80)
        print("🏆 REPORTE FINAL - LLM PREMIER LEAGUE TESTING SUITE")
        print("=" * 80)
        
        summary = self.master_results['summary']
        
        print(f"\n📊 RESUMEN EJECUTIVO:")
        print(f"   • Tests ejecutados: {summary['total_tests_run']}/{len(self.test_suite)}")
        print(f"   • Tests fallidos: {summary['failed_tests']}")
        print(f"   • Tiempo total: {summary['total_execution_time']/60:.1f} minutos")
        
        # Insights de rendimiento
        if summary.get('performance_insights'):
            perf = summary['performance_insights']
            print(f"\n⚡ RENDIMIENTO:")
            print(f"   • LOCAL: {perf['local_avg_time']:.2f}s promedio")
            print(f"   • CLAUDE AI: {perf['ai_avg_time']:.2f}s promedio")
            print(f"   • Diferencia: {abs(perf['local_faster_by']):.2f}s ({'LOCAL' if perf['local_faster_by'] > 0 else 'CLAUDE AI'} más rápido)")
        
        # Insights de calidad
        if summary.get('quality_insights'):
            qual = summary['quality_insights']
            print(f"\n🎯 CALIDAD:")
            print(f"   • LOCAL: {qual['local_quality']:.2f}/1.0")
            print(f"   • CLAUDE AI: {qual['ai_quality']:.2f}/1.0")
            print(f"   • Mejora: {qual['quality_improvement']:+.2f} ({'CLAUDE AI' if qual['quality_improvement'] > 0 else 'LOCAL'} mejor)")
        
        # Insights de carga
        if summary.get('load_insights'):
            print(f"\n💪 CAPACIDAD DE CARGA:")
            for mode, data in summary['load_insights'].items():
                mode_name = "LOCAL" if 'off' in mode else "CLAUDE AI"
                print(f"   • {mode_name}: {data['max_concurrent_users']} usuarios concurrentes máximo")
        
        # Recomendaciones
        print(f"\n🔍 RECOMENDACIONES:")
        for i, rec in enumerate(self.master_results['recommendations'], 1):
            print(f"   {i}. {rec}")
        
        # Conclusión
        print(f"\n🎯 CONCLUSIÓN:")
        if summary['failed_tests'] == 0:
            print("   ✅ Sistema completamente funcional y optimizado")
            print("   🚀 Listo para producción con ambos modos operativos")
        else:
            print("   ⚠️  Sistema requiere optimizaciones menores")
            print("   🔧 Revisar logs para mejoras específicas")
    
    def save_master_results(self) -> str:
        """Guardar resultados maestros"""
        filename = f"master_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = f"{self.results_dir}/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(self.master_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 Resultados maestros guardados en: {filepath}")
        return filepath
    
    def run_full_suite(self):
        """Ejecutar suite completa de tests"""
        print("🏆 LLM PREMIER LEAGUE - MASTER TESTING SUITE")
        print("=" * 80)
        print("🚀 Ejecutando suite completa de tests de rendimiento")
        print(f"📁 Directorio base: {self.base_dir}")
        print(f"⏱️  Duración estimada: 30-45 minutos")
        
        # Verificar servidor
        print("\n🔍 Verificando servidor API...")
        if not self.check_api_server():
            print("❌ Servidor API no disponible en http://localhost:8080")
            print("   Por favor, ejecuta: python LLM/api_server_optimized.py")
            return False
        print("✅ Servidor API disponible")
        
        # Ejecutar cada test
        for test_name, test_info in self.test_suite.items():
            script_path = f"{self.testing_dir}/{test_info['script']}"
            
            if not os.path.exists(script_path):
                print(f"❌ Script no encontrado: {script_path}")
                self.master_results['test_results'][test_name] = {
                    'success': False,
                    'error': 'Script not found',
                    'execution_time': 0
                }
                continue
            
            # Ejecutar test
            result = self.run_test_script(test_name, script_path)
            self.master_results['test_results'][test_name] = result
            
            # Pausa entre tests
            if test_name != list(self.test_suite.keys())[-1]:  # No pause after last test
                print(f"\n⏳ Pausa de 30 segundos antes del siguiente test...")
                time.sleep(30)
        
        # Analizar y reportar
        self.analyze_results()
        self.print_final_report()
        self.save_master_results()
        
        return True

def main():
    runner = MasterTestRunner()
    success = runner.run_full_suite()
    
    if success:
        print(f"\n🎉 TESTING SUITE COMPLETADA")
        print(f"📊 Revisa los archivos de resultados en: {runner.results_dir}")
    else:
        print(f"\n❌ TESTING SUITE FALLÓ")
        print(f"🔧 Revisa la configuración del servidor y vuelve a intentar")
    
    return success

if __name__ == "__main__":
    main()
