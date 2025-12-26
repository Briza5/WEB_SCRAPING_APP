import smtplib, ssl
import os

# Importujeme potřebné moduly:
# smtplib: Tento modul se stará o odesílání emailů pomocí SMTP protokolu.
# ssl: Tento modul poskytuje TLS/SSL šifrování, které je potřeba pro bezpečné připojení.

# definování funkce a přidání proměnné message - argument obsahuje i předmět
def send_email(message):
    host = "smtp.gmail.com"
    # Zde definujeme SMTP server, který budeme používat.
    # "smtp.gmail.com" je adresa SMTP serveru pro Gmail.

    port = 587
    # Zde definujeme port, na kterém SMTP server naslouchá.
    # Port 587 se standardně používá pro STARTTLS, což je způsob, jak začít nezabezpečené spojení
    # a poté ho upgradovat na zabezpečené (TLS/SSL).

    username = "hbbianalytics@gmail.com"
    # Tvůj Gmail email, ze kterého budeš emaily odesílat.

    password = os.getenv("PYTHON_EMAILING_PASSWORD") 
    # Heslo k aplikaci, které jsi si vygeneroval v nastavení Google účtu.
    # Nikdy zde nepoužívej své hlavní heslo ke Google účtu!
    # heslo je uloženo v proměnných prostředí, ke které přistupujemem přes knihonvu os
    # a funkci getenv

    receiver = "hbbianalytics@gmail.com"
    # Emailová adresa příjemce. Můžeš zde zadat jakoukoliv emailovou adresu.

    context = ssl.create_default_context()
    # Vytvoříme výchozí SSL/TLS kontext.
    # Ten obsahuje nastavení pro šifrování, certifikáty atd.
    # Pomáhá zajistit bezpečné a důvěryhodné spojení se serverem.

     
    try:
        # Blok 'try' se používá pro zachycení chyb (výjimek), které by mohly nastat.
        # Kód uvnitř 'try' bloku se spustí. Pokud nastane chyba, program nespadne,
        # ale přeskočí do bloku 'except'.

        with smtplib.SMTP(host, port) as server:
            # Vytvoříme SMTP objekt a připojíme se k SMTP serveru (host) na daném portu.
            # Používáme 'with' příkaz, který automaticky zajistí správné uzavření spojení,
            # i když dojde k chybě.
            # Zde se připojujeme nezabezpečeně, protože port 587 vyžaduje STARTTLS.

            server.ehlo()
            # Příkaz 'ehlo()' (nebo 'helo()') je první "pozdrav", který klient pošle SMTP serveru.
            # Identifikuje se a server mu odpoví s informacemi o svých schopnostech (např. podpora STARTTLS).

            server.starttls(context=context)
            # Toto je klíčový krok! Zde upgradujeme naše nezabezpečené spojení na zabezpečené (TLS/SSL)
            # pomocí 'starttls()'. Používáme 'context', který jsme si vytvořili dříve.

            server.ehlo()
            # Po upgradu na TLS je dobré znovu poslat 'ehlo()'.
            # Některé SMTP servery (včetně Gmailu) to vyžadují, aby si ověřily,
            # že komunikace probíhá přes zabezpečené spojení.

            server.login(username, password)
            # Přihlásíme se k SMTP serveru pomocí našeho uživatelského jména (emailu) a hesla k aplikaci.
            # Toto ověřuje naši identitu u serveru.

            server.sendmail(username, receiver, message)
            # Odešleme email!
            # První argument je adresa odesílatele (náš email).
            # Druhý argument je adresa příjemce.
            # Třetí argument je samotná zpráva.

        print("Email byl úspěšně odeslán!")
        # Pokud se vše odešle bez chyby, vytiskneme potvrzovací zprávu.

    except Exception as e:
        # Pokud v bloku 'try' nastane jakákoliv chyba, tento blok 'except' ji zachytí.
        # 'e' je proměnná, do které se uloží samotná chyba.
        print(f"Při odesílání emailu nastala chyba: {e} s {username} {password}")
        # Vypíšeme chybovou zprávu, abychom věděli, co se pokazilo.

if __name__ == "__main__":    
    send_email("Subject: Test Email\n\nThis is a test email from Python.")