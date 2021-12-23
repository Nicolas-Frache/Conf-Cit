/**
 * Initialisation des handlers sur les deux boutons de base
 */
const init = function () {
    document.getElementById("ajouter_question")
        .addEventListener('click', ajouterQuestion);

    document.getElementById("retirer_question")
        .addEventListener('click', retirerQuestion);

    // Ajout de la première question
    ajouterQuestion();
}

/**
 * Mise à jour du nombre de question dans la champs de formulaire caché associé
 */
const updateNbQuestion = function () {
    document.getElementById("nb_questions").value = nbQuestions;
}

/**
 * Mise à jour du nombre de choix QCM de la question dans le champs de formulaire chaché
 * @param numQ - numéro de la question
 */
const updateNbChoixQcm = function (numQ) {
    document.getElementById("nb_choix_qcm_" + numQ).value = nbChoixParQuestion[numQ - 1];
}

/**
 *  Ajout d'une question dans le html
 */
const ajouterQuestion = function () {
    nbQuestions++;
    nbChoixParQuestion.push(0);
    // Mise à jour du DOM
    insertNewQuestion(nbQuestions);
    updateNbQuestion();
}

/**
 *  Supression d'une question
 */
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
    // On le retire du tableau des choix
    nbChoixParQuestion.pop();
}

/**
 * Passe une question du mode texte au mode QCM
 * @param numQ - Numéro de la question
 */
const chargerQCM = function (numQ) {
    let HTML = `
    <ul>
    </ul>
    <div class="center">
        <input id="qcm_add_${numQ}" class="submit_btn" type="button" value="+">
        <input id="qcm_del_${numQ}" class="submit_btn" type="button" value="-">
    </div>
        `
    // Ajout dans le DOM
    document.getElementById("qcm_choix_zone_" + numQ).innerHTML = HTML;

    // Ajout des listeners pour ajouter et retirer des choix
    let add_btn = document.getElementById("qcm_add_" + numQ);
    document.getElementById("qcm_add_" + numQ).addEventListener("click", function () {
        ajouterChoixQCM(numQ)
    });
    document.getElementById("qcm_del_" + numQ).addEventListener("click", function () {
        retirerChoixQCM(numQ)
    });

    // Ajout des deux choix initiaux
    ajouterChoixQCM(numQ);
    ajouterChoixQCM(numQ);
}

/**
 * Passe une question du mode QCM au mode texte
 * @param numQ - numéro de la question
 */
const dechargerQCM = function (numQ) {
    document.getElementById("qcm_choix_zone_" + numQ).innerHTML = "";
    nbChoixParQuestion[numQ - 1] = 0;
}

/**
 * Ajoute un choix à une question de type QCM
 * @param numQ - numéro de la question
 */
const ajouterChoixQCM = function (numQ) {
    nbChoixParQuestion[numQ - 1]++;
    let numChoix = nbChoixParQuestion[numQ - 1];
    let HTML = `
            <li><input type="text" class="longInput" name="qcm-${numQ}-${numChoix}" required=""
            placeholder="Saisir choix ${numChoix}"></li>
        `
    let element = document.createElement("li");
    element.innerHTML = HTML;
    document.getElementById("qcm_choix_zone_" + numQ).children[0].appendChild(element);
    updateNbChoixQcm(numQ);
}

/**
 * Retire le dernier choix à une question de type QCM, le nombre de choix est au
 * minimun de deux
 * @param numQ - numéro de question
 */
const retirerChoixQCM = function (numQ) {
    if (nbChoixParQuestion[numQ - 1] <= 2) {
        return;
    }
    nbChoixParQuestion[numQ - 1]--;
    let lastChoix = document.getElementById("qcm_choix_zone_" + numQ).children[0].lastElementChild;
    lastChoix.parentNode.removeChild(lastChoix);
    updateNbChoixQcm(numQ);
}

/**
 * Insère dans le DOM le html nécessaire à la création d'une question
 * @param n - Numéro de la question à insérer
 */
const insertNewQuestion = function (n) {
    let HTML = `
            <h2>Question #${n}</h2>
            <div class="form">
                <h2>Intitulé de la question</h2>
                <textarea class="longInput" name="q_${n}" rows="2" cols="60"
                          placeholder="Saisir l'intitulé de la question" required=""></textarea>
                <h2>Selection du type de réponse</h2>
                
                <input class="radio_btn" id="${n}-1" type="radio" name="radio_${n}" value="1" 
                    onchange="dechargerQCM(${n})" checked>
                <label for="${n}-1">Réponse texte</label>
                
                <input class="radio_btn"  id="${n}-2" type="radio" name="radio_${n}" value="2"
                    onchange="chargerQCM(${n})">
                <label for="${n}-2">Réponse à choix multiples</label>
                
                <input type="hidden" id="nb_choix_qcm_${n}" name="nb_choix_qcm_${n}" value="0"/>
                <div class="qcm_choix_zone" id="qcm_choix_zone_${n}">
                </div>
            </div>
        `
    let newdiv = document.createElement("div");
    newdiv.innerHTML = HTML;
    newdiv.classList.add("question")
    document.getElementById("questions").appendChild(newdiv);
}


// Initialisation au chargement de la page

// tableau qui pour chaque question associe le nombre de choix QCM, donc zéro pour les questions textes
let nbChoixParQuestion = [];
let nbQuestions = 0;
window.addEventListener("load", init);