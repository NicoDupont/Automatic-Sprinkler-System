<!doctype html>
<html lang="fr">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<!--<meta http-equiv="refresh" content="15">-->
		<link href="css/bootstrap.min.css" rel="stylesheet">
		<link href="css/css.css" rel="stylesheet">
		<title>Parametrage Sequence</title>
	</head>
	<body>
		<div class="container">
			<div class="row">
				<div class="col-md-12" id="head">
					<a class="btn btn-primary" href="arrosage.html" role="button">Return</a>
				</div>
			</div>
            <div class="row">
                <div class="col-md-6">
	<form id="formseq" method="post" action="#">
    <div class="row">
        <div class="col-md-12">
            <div class="form-group">
            
                <input type="hidden" id="seqid" name="seqid" value="<?php echo $_GET["sequence"];?>" />
            </div>
        </div>
    </div>
    <div class="row">
	<div class="col-md-12">
			<button type="submit" class="btn btn-primary">Maj</button>	
	</div>
    </div>
    <div class="row">
        <div class="col-md-12">
            <div class="form-group">
                <label class="checkbox-inline">Sequence Active : <input type="checkbox"  id="active" name="active" value="yes" checked="true"></label>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-md-12">
            <div class="form-group">
                <label for="heure">Heure Début : <span id="heurevalue"></span> Heure</label>
                <input type="range" min="0" max="23" value="" step="1" class="form-control slider" id="heure" name="heure">
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-md-12">
            <div class="form-group">
                <label for="minute">Minute Début : <span id="minutevalue"></span> Minute</label>
                <input type="range" min="0" max="59" value="" step="1" class="form-control slider" id="minute" name="minute">
            </div>
        </div>
    </div>

    <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label class="checkbox-inline">Tous les jours : <input type="checkbox"  id="touslesjours" name="touslesjours" value="yes" checked="true"></label>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label class="checkbox-inline">Lundi : <input type="checkbox"  id="lundi" name="lundi" value="yes" checked="true"></label>

                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label class="checkbox-inline">Mardi : <input type="checkbox"  id="mardi" name="mardi" value="yes" checked="true"></label>
                        <!--<input type="hidden" name="ifttt" value="0" />-->
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label class="checkbox-inline">Mercredi : <input type="checkbox"  id="mercredi" name="mercredi" value="yes" checked="true"></label>
                        <!--<input type="hidden" name="ifttt" value="0" />-->
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label class="checkbox-inline">Jeudi : <input type="checkbox"  id="jeudi" name="jeudi" value="yes" checked="true"></label>
                        <!--<input type="hidden" name="ifttt" value="0" />-->
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label class="checkbox-inline">Vendredi : <input type="checkbox"  id="vendredi" name="vendredi" value="yes" checked="true"></label>
                        <!--<input type="hidden" name="ifttt" value="0" />-->
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label class="checkbox-inline">Samedi : <input type="checkbox"  id="samedi" name="samedi" value="yes" checked="true"></label>
                        <!--<input type="hidden" name="ifttt" value="0" />-->
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label class="checkbox-inline">Dimanche : <input type="checkbox"  id="dimanche" name="dimanche" value="yes" checked="true"></label>
                        <!--<input type="hidden" name="ifttt" value="0" />-->
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label class="checkbox-inline">Jour Paire : <input type="checkbox"  id="even" name="even" value="yes" checked="true"></label>
                        <!--<input type="hidden" name="ifttt" value="0" />-->
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label class="checkbox-inline">Jour Impaire : <input type="checkbox"  id="odd" name="odd" value="yes" checked="true"></label>
                        <!--<input type="hidden" name="ifttt" value="0" />-->
                    </div>
                </div>
            </div>
		</form>
        </div>

		</div>
		<script src="js/jquery.js"></script>
		<script src="js/sequence.js"></script>
	</body>
</html>
