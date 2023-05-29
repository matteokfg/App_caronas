var opcoes = document.getElementById("id_motorista").options;
  for (var i = 0; i < opcoes.length; i++) {
    if (opcoes[i].value == "{{ motorista.id }}") {
      opcoes[i].selected = true;
    }
  }