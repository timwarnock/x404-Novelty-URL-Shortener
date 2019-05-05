<?php
# vim: set fileencoding=utf-8 tabstop=4 shiftwidth=4 autoindent smartindent:
##
# PROOF-of-CONCEPT for PHP wrapper into x404.db
# currently does not support CJK, hangul or any of the unicode range decodings
#
#
##


# Set internal character encoding to UTF-8
mb_internal_encoding("UTF-8");

# set the path to the db
$DATABASE_PATH = 'sqlite:x404.db';

#
# supported encodings
$_ENC = array(
    'top16' => 'fwmucldrhsnioate',
    'base62' => '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'greek' => 'ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω',
    'greek' => 'ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω',
    'anglosaxon' => 'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
);

function _is_enc($nstr, $enc) {
    foreach (preg_split('//u', $nstr, null, PREG_SPLIT_NO_EMPTY) as $c) {
        if (mb_strpos($enc,$c) === FALSE)
            return FALSE;
    }
    return TRUE;
}

function _decode($nstr, $enc) {
    $base = mb_strlen($enc);
    $basem = 1;
    $n = 0;
    foreach (preg_split('//u', $nstr, null, PREG_SPLIT_NO_EMPTY) as $c) {
        $n += mb_strpos($enc,$c) * $basem;
        $basem = $basem * $base;
    }
    return $n;
}

# 
$rowid = 0;
$newURL = FALSE;
$lookupkey = urldecode(trim($_SERVER['REQUEST_URI'],'/'));
if (strlen($lookupkey)>0) {
    if ($lookupkey[0] == '-') {
        $rowid = _decode(trim($lookupkey,'-'), $_ENC['base62']);
    } elseif (_is_enc($lookupkey, $_ENC['top16'])) {
        $rowid = _decode($lookupkey, $_ENC['top16']);
    } elseif (_is_enc($lookupkey, $_ENC['base62'])) {
        $rowid = _decode($lookupkey, $_ENC['base62']);
    } elseif (_is_enc($lookupkey, $_ENC['greek'])) {
        $rowid = _decode($lookupkey, $_ENC['greek']);
    } elseif (_is_enc($lookupkey, $_ENC['anglosaxon'])) {
        $rowid = _decode($lookupkey, $_ENC['anglosaxon']);
    }
}



# query URLS.db
if ($rowid > 0) {
    $dbh  = new PDO($DATABASE_PATH) or die("cannot open the database");
    $query =  $dbh->prepare("SELECT url FROM urls WHERE rowid= :rowid");
    $query->bindParam(':rowid', $rowid);
    $query->execute();
    $result = $query->fetchAll();
    if (count($result) > 0) {
        $newURL = $result[0]['url'];
    }
}


#print "yes<br> $lookupkey $rowid $newURL"; exit;

if ($newURL) {
  header("Location:$newURL");
  exit;
}

http_response_code(404);
print "404 Not Found";
?>
