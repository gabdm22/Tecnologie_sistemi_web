function stampaCertificato(nome, autore, data, prezzo){
    document.getElementById('cert-nome-opera').innerText = nome;
    document.getElementById('cert-autore-opera').innerText = autore;
    document.getElementById('cert-data').innerText = data;
    document.getElementById('cert-prezzo').innerText = parseFloat(prezzo).toFixed(2);

    window.print();
}