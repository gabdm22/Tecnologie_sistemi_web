function rimuoviDaCollezione(id_ordine, id_opera, nome_opera){
    if(confirm("Sei sicuro di voler eliminare l'opera '" + nome_opera + "' dalla tua collezione?")){
        window.location.href = "/rimuovi/" + id_ordine + "/" + id_opera;
    }
}