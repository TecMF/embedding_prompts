# Classe contendo um dicionário com as informações de cada termo
from typing import Dict


class Queries:

    def __init__(self):
        # Dicionário com as informações dos termos
        self._infos = {}
        self._infos["advanced_persistent_threats"] = {
            "queries_pt": ["APT", "ameaça", "ameaças", "persistente", "persistentes", "avançada", "adversário", "exfiltração", "minar", "objetivos"],
            "queries_en": ["APT", "advanced", "persistent", "threat", "threats", "persistent", "advanced", "adversary", "exfiltration", "mine", "objectives"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["attack"] = {
            "queries_pt": ["ataque", "tentativa", "acesso", "danificar", "interromper", "maliciosa", "degradar", "destruir"],
            "queries_en": ["attack", "attempt", "access", "damage", "interrupt", "malicious", "degrade", "destroy"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["attack_pattern"] = {
            "queries_pt": ["evento", "comportamento", "ataque", "padrão", "violação"],
            "queries_en": ["event", "behavior", "behaviour", "attack", "pattern", "violation"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["attack_scenario"] = {
            "queries_pt": ["cenário", "ataque", "infecção", "intrusão", "ddos", "desfiguração", "playbook", "golpe"],
            "queries_en": ["scenario", "attack", "infection", "intrusion", "ddos", "disfiguration", "playbook", "compromise"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["attack_vector"] = {
            "queries_pt": ["vetor", "ataque", "método", "métodos", "técnica", "técnicas", "acesso"],
            "queries_en": ["vector", "attack", "method", "methods", "technique", "techniques", "access"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["attacker"] = {
            "queries_pt": ["ataque", "atacante", "indivíduo", "grupo", "organização", "governo", "atividades", "prejudiciais", "intenção", "maliciosa"],
            "queries_en": ["attack", "attacker", "individual", "group", "organization", "organisation", "government", "activities", "prejudicial", "intention", "malicious"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["backdoor"] = {
            "queries_pt": ["backdoor", "vulnerabilidade", "ferramenta", "comprometimento", "invasor", "acesso", "malware", "risco"],
            "queries_en": ["backdoor", "vulnerability", "tool", "compromise", "invader", "access", "malware", "risk"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["campaign"] = {
            "queries_pt": ["campanha", "agrupamento", "atividades", "intrusão", "período", "alvos", "objetivos"],
            "queries_en": ["campaign", "grouping", "activities", "intrusion", "period", "targets", "objectives"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["characteristic"] = {
            "queries_pt": ["característica", "características", "elemento", "conceitual", "estratégico", "domínio", "estruturadas"],
            "queries_en": ["characteristic", "characteristics", "element", "conceptual", "strategic", "domain", "structured"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["consequence"] = {
            "queries_pt": ["consequência", "efeito", "evento", "incidente", "ocorrência", "perda", "confidencialidade", "integridade", "disponibilidade"],
            "queries_en": ["consequence", "effect", "event", "incident", "occurrence", "loss", "confidentiality", "integrity", "availability"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["countermeasure"] = {
            "queries_pt": ["contramedida", "método", "métodos", "reativo", "reativos", "evitar", "exploração", "ameaça", "prevenção", "patches", "controle", "acesso", "segurança", "controle"],
            "queries_en": ["countermeasure", "method", "methods", "reactive", "avoid", "exploitation", "threat", "prevention", "patches", "control", "access", "security", "control"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["course_of_action"] = {
            "queries_pt": ["curso", "ação", "medidas", "resposta", "riscos", "modelo", "estágios", "identificar", "fases", "reconhecimento", "armamento", "entrega", "exploração", "instalação", "comando", "controle", "ações", "monetização"],
            "queries_en": ["course", "action", "measures", "response", "risks", "model", "stages", "identify", "phases", "reconnaissance", "weaponization", "delivery", "exploitation", "installation", "command", "constrol", "actions", "monetization"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["damage"] = {
            "queries_pt": ["dano", "efeito", "evento", "incidente", "ocorrência", "perda"],
            "queries_en": ["damage", "effect", "event", "incident", "occurrence", "loss"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["event"] = {
            "queries_pt": ["evento", "ocorrência", "observável", "indicação", "indicente", "suspeita", "adverso"],
            "queries_en": ["event", "occurrence", "observable", "indication", "incident", "suspicion", "adverse"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["impact"] = {
            "queries_pt": ["impacto", "efeito", "evento", "incidente", "ocorrência", "perda", "dano", "valor", "utilidade", "função"],
            "queries_en": ["impact", "effect", "event", "incident", "occurrence", "loss", "damage", "value", "utility", "function"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["incident"] = {
            "queries_pt": ["indicente", "ocorrência", "risco", "confidencialidade", "integridade", "disponibilidade", "informações", "violação", "ameaça", "políticas"],
            "queries_en": ["incident", "occurrence", "risk", "confidentiality", "integrity", "availability", "information", "violation", "threat", "policies"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["incident_handling_steps"] = {
            "queries_pt": ["passos", "lidar", "incidentes", "mitigação", "violação", "práticas", "etapas", "preparação", "identificação", "remediação", "lições"],
            "queries_en": ["incident", "handling", "steps", "violation", "practices", "stages", "preparation", "identification", "remediation", "lessons"],
            "top_n": 10,
            "vizinhos": 0,
        }
        self._infos["information_asset"] = {
            "queries_pt": ["ativo", "asset", "informação", "valor", "pessoa", "organização", "meio", "recurso", "crítico"],
            "queries_en": ["asset", "information", "value", "person", "organization", "organisation", "medium", "resource", "critical"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["location"] = {
            "queries_pt": ["localização", "lugar", "posição", "local"],
            "queries_en": ["location", "place", "position", "particular"],
            "top_n": 3,
            "vizinhos": 0,
        }
        self._infos["malware"] = {
            "queries_pt": ["malware", "código", "software", "malicioso", "compromete", "processo", "danificar", "vírus", "ransomware", "trojan", "firmware", "troia", "infecta", "spyware"],
            "queries_en": ["malware", "code", "software", "malicious", "compromises", "process", "damage", "virus", "ransomware", "trojan", "firmware", "infects", "spyware"],
            "top_n": 5,
            "vizinhos": 0,
        }
        self._infos["malware_family"] = {
            "queries_pt": ["malware", "software", "maliciosos", "categoria", "vírus", "ransomware", "worms", "spyware"],
            "queries_en": ["malware", "software", "malicious", "category", "virus", "ransomware", "worms", "spyware"],
            "top_n": 5,
            "vizinhos": 0,
        }
        self._infos["mitigation"] = {
            "queries_pt": ["mitigação", "curso", "ação", "medida", "estratégia", "prevenir", "reduzir", "proteger"],
            "queries_en": ["mitigation", "course", "action", "measure", "strategy", "prevent", "reduce", "protect"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["motivation"] = {
            "queries_pt": ["motivação", "motivo", "atacante", "executar", "planejar", "ataque", "ganho", "perda"],
            "queries_en": ["motivation", "motive", "attacker", "execute", "plan", "attack", "gain", "loss"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["organization"] = {
            "queries_pt": ["organização", "entidade", "estrutura", "tamanho", "posicionamento"],
            "queries_en": ["organization", "organisation", "entity", "structure", "site", "positioning"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["playbook"] = {
            "queries_pt": ["playbook", "procedimento", "defesa", "procedimentos", "planejamento", "condução", "atividades", "resposta", "incidentes", "vulnerabilidades"],
            "queries_en": ["playbook", "procedure", "defense", "procedures", "planning", "conduction", "activities", "response", "incidents", "vulnerabilities"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["process"] = {
            "queries_pt": ["processo", "atividades", "interativas", "interrelacionadas", "entradas", "resultado"],
            "queries_en": ["process", "activities", "interactive", "interrelated", "inputs", "result"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["ransomware"] = {
            "queries_pt": ["ransomware", "malware", "extorsão", "disco", "rígido", "negando", "nega", "acesso", "negado", "arquivos", "resgate", "criptografa"],
            "queries_en": ["ransomware", "malware", "extorsion", "harddrive", "denying", "denies", "access", "denied", "files", "ransom", "encrypts"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["risk"] = {
            "queries_pt": ["risco", "nível", "ameaça", "vulnerabilidade", "probabilidade", "ataque"],
            "queries_en": ["risk", "level", "threat", "vulnerability", "probability", "attack"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["security_property"] = {
            "queries_pt": ["propriedade", "segurança", "princípio", "característica", "princípios", "características", "disponibilidade", "integridade", "autenticidade", "privacidade", "auditabilidade", "legalidade"],
            "queries_en": ["property", "security", "principle", "characteristic", "principles", "characteristics", "availability", "integrity", "authenticity", "privacy", "auditability", "legality"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["software"] = {
            "queries_pt": ["software", "código", "programa", "programas", "computador", "hardware", "dados", "associados", "modificados", "dinamicamente", "bibliotecas"],
            "queries_en": ["software", "code", "program", "programs", "computer", "hardware", "data", "associated", "modified", "dinamically", "libraries"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["system"] = {
            "queries_pt": ["sistema", "elementos", "interativos", "propósitos", "tipos", "software", "hardware", "humanos", "processos", "entidades"],
            "queries_en": ["system", "elements", "interactive", "purposes", "types", "software", "hardware", "humans", "processes", "entities"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["tactic"] = {
            "queries_pt": ["tática", "objetivo", "estratégico", "adversário"],
            "queries_en": ["tactic", "objective", "stratgic", "adversary"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["technique"] = {
            "queries_pt": ["técnica", "adversário", "objetivo", "tático"],
            "queries_en": ["technique", "adversary", "objective", "tactical"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["technology"] = {
            "queries_pt": ["tecnologia", "informação", "equipamento", "sistema", "interconectado", "subsistema", "dados", "informações", "processa", "transmite"],
            "queries_en": ["technology", "information", "equipment", "system", "interconnectec", "subsystem", "data", "information", "processes", "transmits"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["threat"] = {
            "queries_pt": ["ameaça", "potencial", "violação", "segurança", "ação", "evento", "violar", "danos", "dano", "explorar", "vulnerabilidades", "impacto", "negativo", "negativamente", "adversamente", "explorar", "perigo"],
            "queries_en": ["threat", "potential", "violation", "security", "action", "event", "violate", "damage", "exploit", "vulnerabilities", "impact", "negative", "negatively", "adversely", "danger"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["threat_actor"] = {
            "queries_pt": ["ator", "ameaça", "indivíduo", "grupo", "organização", "governo", "atividades", "prejudiciais"],
            "queries_en": ["actor", "threat", "individual", "group", "organization", "organisation", "activities", "detrimental"],
            "top_n": 6,
            "vizinhos": 0,
        }
        self._infos["vulnerability"] = {
            "queries_pt": ["vulnerabilidade", "fraqueza", "característica", "ativo", "organização", "exploração", "ameaça", "suscetível", "perigo"],
            "queries_en": ["vulnerability", "weakness", "characteristic", "asset", "organization", "organisation", "threat", "susceptible", "danger"],
            "top_n": 6,
            "vizinhos": 0,
        }
    
    def getAllInformation(self) -> Dict:
        """
        Obtém as informações de BM25 de todos os termos a serem buscados.
        
        Returns:
            Dict: informações de todos os termos.
        """
        return self._infos

    def getInformation(self, id: str) -> Dict:
        """
        Obtém as informações de BM25 de um termo a ser buscado.
        
        Args:
            id (str): identificador do termo (checar nos diretórios).
        
        Returns:
            Dict: informações do termo buscado.
        """
        return self._infos(id)