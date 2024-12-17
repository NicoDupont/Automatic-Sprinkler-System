<!doctype html>
<html lang="fr">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<!--<meta http-equiv="refresh" content="15">-->
		<link href="css/bootstrap.min.css" rel="stylesheet">
		<link href="css/css.css" rel="stylesheet">
		<title>Parametrage Zone</title>
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
	<form id="formzone" method="post" action="#">

    <input type="hidden" id="idsv" name="idsv" value="<?php echo $_GET["zone"];?>" />
    <input type="hidden" id="typesv" name="typesv" value="<?php echo $_GET["type"];?>" />
    <div class="row">
        <div class="col-md-12">
                <button type="submit" class="btn btn-primary">Maj</button>	
        </div>
    </div>

    <div class="row">
        <div class="col-md-12">
            <div class="form-group">
                <label class="checkbox-inline">Zone Open (mode manuel) : <input type="checkbox"  id="open" name="open" value="yes" checked="true"></label>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-md-12">
            <div class="form-group">
                <label class="checkbox-inline">Zone Active : <input type="checkbox"  id="active" name="active" value="yes" checked="true"></label>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-md-12">
            <div class="form-group">
                <label for="code">Code Zone :</label>
                <input type="text" value="" class="form-control" id="code" name="code">
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-md-12">
            <div class="form-group">
            <label for="nom">Nom Zone : </label>
                <input type="text" value="" class="form-control" id="nom" name="nom">
            </div>
        </div>
    </div>


    <div class="row">
        <div class="col-md-12">
            <div class="form-group">
                <label for="numero">Numéro : <span id="numerovalue"></span> #</label>
                <input type="range" min="1" max="22" value="" step="1" class="form-control slider" id="numero" name="numero">
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-md-12">
            <div class="form-group">
                <label for="sequence">Sequence : <span id="sequencevalue"></span></label>
                <select id="sequence" name="sequence" class="form-select">
                    <option value="S1">S1</option>
                    <option value="S2">S2</option>
                    <option value="S3">S3</option>
                </select>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-md-12">
            <div class="form-group">
                <label for="gpio">Gpio N° : <span id="gpiovalue"></span></label>
                <input type="range" min="1" max="30" value="" step="1" class="form-control slider" id="gpio" name="gpio">
            </div>
        </div>
    </div>
      <div class="row">
        <div class="col-md-12">
            <div class="form-group">
                <label for="duree">Durée : <span id="dureevalue"></span> Minutes</label>
                <input type="range" min="2" max="180" value="" step="1" class="form-control slider" id="duree" name="duree">
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-md-12">
            <div class="form-group">
                <label for="coef">Coefficient Durée : <span id="coefvalue"></span> %</label>
                <input type="range" min="10" max="300" value="" step="5" class="form-control slider" id="coef" name="coef">
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
		<script src="js/zone.js"></script>
	</body>
</html>
