from typing import Dict, List
import requests

def get_pdb_ids(uniprot_id: str) -> List:

    """
    Retrieve the PDB IDS associated with a UniProtKB entry ID
    """
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    params = {"fields": "xref_pdb"}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        pdb_refs = data.get("uniProtKBCrossReferences", [])
        pdb_ids = [ref["id"] for ref in pdb_refs if ref["database"] == "PDB"]
        return pdb_ids
    else:
        return None


def has_ligands(pdb_id: str) -> Dict:
    """
        Check if a pdb entry has any ligans
    """
    
    # Get entry summary
    entry_url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    entry_response = requests.get(entry_url)
    
    if entry_response.status_code != 200:
        return None
    
    entry_data = entry_response.json()
    
    results = {
        "summary": [],
    }
    
    # Summary counts
    info = entry_data.get("rcsb_entry_info", {})
    results["summary"] = {
        "polymer_entity_count": info.get("polymer_entity_count", 0),
        "nonpolymer_entity_count": info.get("nonpolymer_entity_count", 0),
        "total_chains": info.get("deposited_polymer_monomer_count", 0)
    }
    return results

get_all_binding_partners("3C59")
