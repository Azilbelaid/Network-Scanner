#!/usr/bin/env python3
"""
Network Scanner - Outil d'Analyse Réseau et Sécurité
Auteur: Belaid AZIL
Date: Mars 2026
Description: Scanner de réseau pour découvrir les hôtes actifs, scanner les ports
             et identifier les services. Génère des rapports en TXT et JSON.
"""

import socket
import sys
import json
import argparse
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import ipaddress
import time

class NetworkScanner:
    """Scanner réseau pour analyse de sécurité"""
    
    def __init__(self, timeout=1, max_threads=50):
        """
        Initialise le scanner
        
        Args:
            timeout (int): Timeout pour les connexions en secondes
            max_threads (int): Nombre maximum de threads parallèles
        """
        self.timeout = timeout
        self.max_threads = max_threads
        self.results = {
            'scan_info': {},
            'hosts': {},
            'summary': {}
        }
    
    def scan_port(self, ip, port):
        """
        Scanne un port spécifique sur une IP
        
        Args:
            ip (str): Adresse IP à scanner
            port (int): Numéro de port
            
        Returns:
            dict: Informations sur le port (ouvert/fermé, service)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                # Port ouvert, tenter d'identifier le service
                try:
                    service = socket.getservbyport(port, 'tcp')
                except:
                    service = "unknown"
                
                return {
                    'port': port,
                    'state': 'open',
                    'service': service
                }
            return None
        except socket.timeout:
            return None
        except Exception as e:
            return None
    
    def check_host(self, ip):
        """
        Vérifie si un hôte est actif en testant le port 80
        
        Args:
            ip (str): Adresse IP à vérifier
            
        Returns:
            bool: True si l'hôte répond, False sinon
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, 80))
            sock.close()
            return result == 0
        except:
            # Essayer aussi avec un ping ICMP simulé (port 443)
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, 443))
                sock.close()
                return result == 0
            except:
                return False
    
    def scan_host_ports(self, ip, ports):
        """
        Scanne plusieurs ports sur un hôte
        
        Args:
            ip (str): Adresse IP de l'hôte
            ports (list): Liste des ports à scanner
            
        Returns:
            dict: Résultats du scan pour cet hôte
        """
        print(f"[*] Scan de {ip} en cours...")
        
        host_info = {
            'ip': ip,
            'hostname': self.get_hostname(ip),
            'open_ports': [],
            'scan_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Scanner les ports en parallèle
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_port = {
                executor.submit(self.scan_port, ip, port): port 
                for port in ports
            }
            
            for future in as_completed(future_to_port):
                result = future.result()
                if result:
                    host_info['open_ports'].append(result)
                    print(f"  [+] Port {result['port']} ouvert - Service: {result['service']}")
        
        return host_info
    
    def get_hostname(self, ip):
        """
        Tente de résoudre le nom d'hôte
        
        Args:
            ip (str): Adresse IP
            
        Returns:
            str: Nom d'hôte ou 'unknown'
        """
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return "unknown"
    
    def discover_hosts(self, network):
        """
        Découvre les hôtes actifs sur un réseau
        
        Args:
            network (str): Réseau au format CIDR (ex: 192.168.1.0/24)
            
        Returns:
            list: Liste des IPs actives
        """
        print(f"\n[*] Découverte des hôtes sur {network}...")
        active_hosts = []
        
        try:
            net = ipaddress.ip_network(network, strict=False)
            
            with ThreadPoolExecutor(max_workers=50) as executor:
                future_to_ip = {
                    executor.submit(self.check_host, str(ip)): str(ip)
                    for ip in net.hosts()
                }
                
                for future in as_completed(future_to_ip):
                    ip = future_to_ip[future]
                    if future.result():
                        active_hosts.append(ip)
                        print(f"  [+] Hôte actif trouvé: {ip}")
        
        except Exception as e:
            print(f"[!] Erreur lors de la découverte: {e}")
        
        return active_hosts
    
    def scan_network(self, targets, ports):
        """
        Scanne un réseau complet
        
        Args:
            targets (list): Liste d'IPs ou réseau CIDR
            ports (list): Liste de ports à scanner
        """
        start_time = time.time()
        
        # Informations du scan
        self.results['scan_info'] = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'scanner': 'Network Scanner v1.0',
            'author': 'Belaid AZIL',
            'targets': targets,
            'ports_scanned': len(ports)
        }
        
        print("\n" + "="*60)
        print("  NETWORK SCANNER - Analyse de Sécurité Réseau")
        print("  Auteur: Belaid AZIL")
        print("="*60)
        
        # Scanner chaque cible
        for target in targets:
            # Si c'est un réseau CIDR, découvrir les hôtes d'abord
            if '/' in target:
                active_hosts = self.discover_hosts(target)
                for host in active_hosts:
                    host_results = self.scan_host_ports(host, ports)
                    if host_results['open_ports']:
                        self.results['hosts'][host] = host_results
            else:
                # Scanner directement l'IP
                host_results = self.scan_host_ports(target, ports)
                if host_results['open_ports']:
                    self.results['hosts'][target] = host_results
        
        # Statistiques
        scan_duration = time.time() - start_time
        total_open_ports = sum(len(h['open_ports']) for h in self.results['hosts'].values())
        
        self.results['summary'] = {
            'total_hosts_scanned': len(self.results['hosts']),
            'total_open_ports': total_open_ports,
            'scan_duration_seconds': round(scan_duration, 2)
        }
        
        print("\n" + "="*60)
        print(f"  Scan terminé en {scan_duration:.2f} secondes")
        print(f"  Hôtes avec ports ouverts: {len(self.results['hosts'])}")
        print(f"  Total ports ouverts: {total_open_ports}")
        print("="*60 + "\n")
    
    def generate_txt_report(self, filename='scan_report.txt'):
        """Génère un rapport texte dans le dossier rapports/"""
        # Créer le dossier rapports s'il n'existe pas
        reports_dir = 'rapports'
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
            print(f"[+] Dossier '{reports_dir}/' créé")
        
        # Chemin complet du fichier
        filepath = os.path.join(reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  RAPPORT D'ANALYSE RÉSEAU\n")
            f.write("="*70 + "\n\n")
            
            # Informations du scan
            f.write("INFORMATIONS DU SCAN:\n")
            f.write("-" * 70 + "\n")
            for key, value in self.results['scan_info'].items():
                f.write(f"{key}: {value}\n")
            f.write("\n")
            
            # Résultats par hôte
            f.write("RÉSULTATS PAR HÔTE:\n")
            f.write("-" * 70 + "\n\n")
            
            for ip, host_data in self.results['hosts'].items():
                f.write(f"Hôte: {ip}\n")
                f.write(f"  Nom d'hôte: {host_data['hostname']}\n")
                f.write(f"  Heure du scan: {host_data['scan_time']}\n")
                f.write(f"  Ports ouverts ({len(host_data['open_ports'])}):\n")
                
                for port_info in host_data['open_ports']:
                    f.write(f"    - Port {port_info['port']}/tcp")
                    f.write(f" ({port_info['state']}) - Service: {port_info['service']}\n")
                f.write("\n")
            
            # Résumé
            f.write("="*70 + "\n")
            f.write("RÉSUMÉ:\n")
            f.write("-" * 70 + "\n")
            for key, value in self.results['summary'].items():
                f.write(f"{key}: {value}\n")
            f.write("="*70 + "\n")
        
        print(f"[+] Rapport TXT généré: {filepath}")
    
    def generate_json_report(self, filename='scan_report.json'):
        """Génère un rapport JSON dans le dossier rapports/"""
        # Créer le dossier rapports s'il n'existe pas
        reports_dir = 'rapports'
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        # Chemin complet du fichier
        filepath = os.path.join(reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"[+] Rapport JSON généré: {filepath}")


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description='Network Scanner - Outil d\'analyse réseau et sécurité',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  %(prog)s -t 192.168.1.1 -p 80,443,22
  %(prog)s -t 192.168.1.0/24 -p 1-1024
  %(prog)s -t scanme.nmap.org -p 80,443,8080 --timeout 2
        """
    )
    
    parser.add_argument(
        '-t', '--target',
        required=True,
        help='Cible(s) à scanner (IP, hostname, ou réseau CIDR)'
    )
    
    parser.add_argument(
        '-p', '--ports',
        default='21,22,23,25,80,443,3306,3389,8080',
        help='Ports à scanner (ex: 80,443 ou 1-1000). Défaut: ports communs'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=1,
        help='Timeout pour les connexions (secondes). Défaut: 1'
    )
    
    parser.add_argument(
        '--threads',
        type=int,
        default=50,
        help='Nombre de threads parallèles. Défaut: 50'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='scan_report',
        help='Nom de base pour les fichiers de sortie. Défaut: scan_report'
    )
    
    args = parser.parse_args()
    
    # Parser les ports
    ports = []
    try:
        for port_range in args.ports.split(','):
            if '-' in port_range:
                start, end = map(int, port_range.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(port_range))
    except ValueError:
        print("[!] Format de ports invalide. Utilisez: 80,443 ou 1-1000")
        sys.exit(1)
    
    # Parser les cibles
    targets = [t.strip() for t in args.target.split(',')]
    
    # Créer le scanner
    scanner = NetworkScanner(timeout=args.timeout, max_threads=args.threads)
    
    # Lancer le scan
    try:
        scanner.scan_network(targets, ports)
        
        # Générer les rapports
        scanner.generate_txt_report(f"{args.output}.txt")
        scanner.generate_json_report(f"{args.output}.json")
        
    except KeyboardInterrupt:
        print("\n[!] Scan interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Erreur: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
