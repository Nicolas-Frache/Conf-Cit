<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Envoi d'un message par formulaire</title>
</head>

<body>
    <!- indiquer votre mail pour les tests ->
    <?php
    $retour = mail('clement.wenger@telecomnancy.eu', 'Envoi depuis la page Erreur', $_POST['message'], 'From : conf-civ@telecomnancy.eu');
    if ($retour) {
        echo '<p>Votre message a été envoyé.</p>';
    }
    ?>
</body>
</html>
