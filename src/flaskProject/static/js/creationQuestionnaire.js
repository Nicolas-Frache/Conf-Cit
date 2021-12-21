// Initialisation des handlers sur les deux boutons de base
const init = function () {
    document.getElementById("ajouter_question")
        .addEventListener('click', ajouterQuestion);

    document.getElementById("retirer_question")
        .addEventListener('click', retirerQuestion);

    ajouterQuestion();
}

const updateNbQuestion = function () {
    document.getElementById("nb_questions").value = nbQuestions;
}

// Ajout d'une question dans le html
const ajouterQuestion = function () {
    nbQuestions++;
    nbChoixParQuestion.push(0);
    insertNewQuestion(nbQuestions);
    document.getElementById("nb_questions").value = nbQuestions;
    updateNbQuestion();
}

// Supression d'une question
const retirerQuestion = function () {
    // On ne peut pas supprimer la première question
    if (nbQuestions <= 1) {
        return;
    }
    nbQuestions--;
    updateNbQuestion();
    // Supression de l'élément html
    let lastQuestion = document.getElementById("questions").lastElementChild;
    lastQuestion.parentNode.removeChild(lastQuestion);
    nbChoixParQuestion.pop();

}

const chargerQCM = function (numQ) {
    console.log("chargerQCM: " + numQ)
    let HTML = `
    <ul>
    </ul>
    <div class="center">
        <input id="qcm_add_${numQ}" class="submit_btn" type="button" value="+">
        <input id="qcm_del_${numQ}" class="submit_btn" type="button" value="-">
    </div>
        `
    document.getElementById("qcm_choix_zone_" + numQ).innerHTML = HTML;
    let add_btn = document.getElementById("qcm_add_" + numQ);
    document.getElementById("qcm_add_" + numQ).addEventListener("click", function () {
        ajouterChoixQCM(numQ)
    });
    document.getElementById("qcm_del_" + numQ).addEventListener("click", function(){
        retirerChoixQCM(numQ)
    });
    ajouterChoixQCM(numQ);
    ajouterChoixQCM(numQ);
}

const dechargerQCM = function (numQ) {
    console.log("dechargerQCM: " + numQ)
    document.getElementById("qcm_choix_zone_" + numQ).innerHTML = "";
    nbChoixParQuestion[numQ - 1] = 0;
}

const ajouterChoixQCM = function (numQ) {
    console.log("Ajouter choix: " + numQ);
    nbChoixParQuestion[numQ - 1]++;
    let numChoix = nbChoixParQuestion[numQ - 1];
    let HTML = `
            <li><input type="text" class="longInput" name="qcm-${numQ}-${numChoix}" required=""
            placeholder="Saisir choix ${numChoix}"></li>
        `
    let element = document.createElement("li");
    element.innerHTML = HTML;
    document.getElementById("qcm_choix_zone_" + numQ).children[0].appendChild(element);
}

const retirerChoixQCM = function (numQ) {
    console.log("Retirer choix: " + numQ)
    if (nbChoixParQuestion[numQ - 1] <= 2) {
        return;
    }
    nbChoixParQuestion[numQ - 1]--;
    let lastChoix = document.getElementById("qcm_choix_zone_"+numQ).children[0].lastElementChild;
    lastChoix.parentNode.removeChild(lastChoix);
}

const insertNewQuestion = function (n) {
    let HTML = `
    <div class="question">
            <h2>Question #${n}</h2>
            <div class="form">
                <h2>Intitulé de la question</h2>
                <textarea class="longInput" name="q_${n}" rows="2" cols="60"
                          placeholder="Saisir l'intitulé de la question"></textarea>
                <h2>Selection du type de réponse</h2>
                
                <input class="radio_btn" id="${n}-1" type="radio" name="radio_${n}" value="1" 
                    onchange="dechargerQCM(${n})" checked>
                <label for="${n}-1">Réponse texte</label>
                
                <input class="radio_btn"  id="${n}-2" type="radio" name="radio_${n}" value="2"
                    onchange="chargerQCM(${n})">
                <label for="${n}-2">Réponse à choix multiples</label>
                
                <div class="qcm_choix_zone" id="qcm_choix_zone_${n}"></div>
            </div>
    </div>
        `
    let newdiv = document.createElement("div");
    newdiv.innerHTML = HTML;
    document.getElementById("questions").appendChild(newdiv);
}

let nbChoixParQuestion = [];
let nbQuestions = 0;
window.addEventListener("load", init);
