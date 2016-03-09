# jizdoteka-web

[![Gitter](https://badges.gitter.im/jizdoteka/general.svg)](https://gitter.im/jizdoteka/general?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


***Nelíbí se Ti BlaBlaCar?
Ani nám!
Pojdme spolu udělat něco lepšího.***

Proč?
Jako náhrada jízdomatu a protože blablacar nám nevyhovuje (je komerční a po čase si ve většině zemí začíná účtovat cca 10% poplatky).

Co chceme?
 * Nekomerční aplikaci (žádné poplatky!)
 * Svobodu v určování cen jízdného a žádnou cenzuru
 * Dělat to pro sebe
 * Být otevření změnám - každý se může zapojit

Jak?
* Vlastní open-source aplikace na www.jizdoteka.cz
* Inspirujeme se jízdomatem
* Nepřevezmeme chyby blablacaru







## Instalace

Pro účely vývoje/testování doporučuji použít `virtualenv` (`pip3 install virtualenv`, nebo `dnf install python3-virtualenv`).

Projekt je stavěn na frameworku Django 1.9 pro Python 3.4 (a vyšší).

Stáhnutí zdrojových kódů:
```
git clone https://github.com/jizdoteka/jizdoteka-web.git
cd jizdoteka-web
```

Založíme virtualenv prostředí (například `venv`) a nainstalujeme závislosti:
```
virtualenv-3.4 venv
source venv/bin/activate
pip3 install -r requirements.txt
git clone https://github.com/harmo/django-email-as-username.git
python django-email-as-username/setup.py install
```

Spuštění serveru: `./manage.py runserver`

> Web je dostupný na: `http://localhost:8000`
>
> Administrace (admin/admin): `http://localhost:8000/admin`

Pokud jste provedli nějaké změny v modelech, je nutné vytvořit migrace DB pomocí:
```
./manage.py makemigrations
```
a následně je aplikovat:
```
./manage.py migrate
```

## Stav projektu
Rozpracováno (částečně funguje):
 * model DB, dost tam toho ještě chybí, ale to nejdůležitější (jízdy jako takové) jsou z velké části udělané. Počítám s tím, že se lidé mohou přihlásit jen na část trasy, cena za úsek je nepovinná
 * výpis jízd
 * detail vybrané jízdy - vč. přihlášených lidí na úsecích
 * vytvoření a editace existující jízdy

Chybí, je třeba opravit (hmm.. od čeho začít :)
 * plnění webu day prozatím pouze skrze administraci (viz. link výše)

 * front-end, design
 * hodnocení jízd
 * poptávky jízd
 * (a všechno ostatní ...)

 * (skrze administraci) lze přihlásit pasažéra i na trasu mimo jeho jízdu - toto budeme stejně ošetřovat už při vkládání do DB, takže to nakonec tak moc vadit nebude
 * všechno ostatní ...

## Zavislosti
 * je potreba rucne doinstalovat emailusernames, pip nefunguje (nevim proc)
 * https://github.com/harmo/django-email-as-username
