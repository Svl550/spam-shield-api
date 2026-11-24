"""
Base de données haute performance des domaines temporaires et jetables (Spam / Burner domains).
Optimisé sous forme de Set pour recherche O(1).
"""

DISPOSABLE_DOMAINS = {
    # Domaines jetables ultra-courants
    "10minutemail.com", "10minutemail.net", "10minmail.com", "20minutemail.com",
    "yopmail.com", "yopmail.fr", "yopmail.net", "cool.fr.nf", "jetable.fr.nf",
    "guerrillamail.com", "guerrillamail.net", "guerrillamail.biz", "guerrillamail.org",
    "sharklasers.com", "grr.la", "guerrillamailblock.com", "pokemail.net",
    "mailinator.com", "mailinator.net", "mailin8r.com", "suremail.info", "spamherelots.com",
    "temp-mail.org", "tempmail.net", "tempmail.com", "temp-mail.io", "dispostable.com",
    "trashmail.com", "trashmail.net", "trashmail.org", "trashmail.me", "fakemailgenerator.com",
    "throwawaymail.com", "getairmail.com", "generator.email", "mohmal.com", "crazymailing.com",
    "emailondeck.com", "burnerdelivery.com", "inboxkitten.com", "nada.ltd", "getnada.com",
    "mytemp.email", "luxusmail.org", "tempr.email", "dropmail.me", "anonymbox.com",
    "burnermail.io", "maildrop.cc", "harakirimail.com", "dayrep.com", "einrot.com",
    "fleckens.com", "gustr.com", "jourrapide.com", "rhyta.com", "superrito.com",
    "teleworm.us", "armyspy.com", "cuvox.de", "fakeinbox.com", "mailcatch.com",
    "mintemail.com", "spambog.com", "spamgourmet.com", "trash-mail.com", "kasmail.com",
    "deadaddress.com", "spamex.com", "mailnull.com", "incognitomail.org", "jetable.org",
    "0-mail.com", "0815.ru", "0clickemail.com", "10mail.org", "123-m.com", "1clickmail.com",
    "2prong.com", "30minutemail.com", "3d-painting.com", "4warding.com", "5ymail.com",
    "60minutemail.com", "675hosting.com", "7tags.com", "9ox.net", "a-bc.net", "afrobacon.com",
    "ajaxapp.net", "amilearth.com", "amiri.net", "amiriindustries.com", "anonbox.net",
    "antichef.com", "antichef.net", "antireg.ru", "antispam.de", "baxomale.ht.cx",
    "beefmilk.com", "binkmail.com", "bio-muesli.net", "bobmail.info", "bodhi.lawlita.com",
    "bofthew.com", "boun.cr", "bouncr.com", "breakthru.com", "brefmail.com", "broadbandninja.com",
    "bsnow.net", "bugmenot.com", "bumpymail.com", "casualdx.com", "centermail.com",
    "centermail.net", "chogmail.com", "choicemail1.com", "clipmail.eu", "cmail.club",
    "cosmorph.com", "courrieltemporaire.com", "cubiclink.com", "curryrasen.de", "cust.in",
    "dacoolest.com", "dandikmail.com", "deadchildren.org", "despam.it", "despammed.com",
    "devnullmail.com", "dfgh.net", "digitalsanctuary.com", "dingbone.com", "discard.email",
    "discardmail.com", "discardmail.de", "disposableaddress.com", "disposableinbox.com",
    "disposeamail.com", "disposemail.com", "dm.is", "dodgeit.com", "dodgit.com", "dontext.com",
    "dontreg.com", "dontsendmespam.de", "drdrb.net", "dump-email.info", "dumpmail.de",
    "dumpyemail.com", "e4ward.com", "easytrashmail.com", "ebeschwerde.de", "eintagsmail.de",
    "email60.com", "emailinfive.com", "emailmiser.com", "emailproxsy.com", "emailsensei.com",
    "emailtemporaneo.net", "emailwarden.com", "emailx.at.tc", "emailxfer.com", "emeil.in",
    "emeil.ir", "emz.net", "ephemail.net", "etranquille.net", "evopo.com", "expirmail.com",
    "extantmails.com", "eyepaste.com", "ezfill.com", "fastchevrons.com", "filzmail.com",
    "fixmail.it", "flyspam.com", "front14.org", "fudgerub.com", "fux0ringduh.com",
    "garbagemail.org", "gelbfieber.de", "get1mail.com", "get2mail.fr", "giantmail.de",
    "gishpuppy.com", "greensloth.com", "gsrv.co.uk", "guerillamail.com", "h8s.org",
    "haltospam.com", "hidemail.de", "hotpop.com", "hulapla.de", "hushmail.me", "hushmail.net",
    "ieatspam.com", "ignorelist.com", "ihatespam.ca", "ikbenspamvrij.nl", "imails.info",
    "inboxclean.com", "inboxclean.org", "incognitomail.com", "incognitomail.net", "insorg-mail.info",
    "instantemailaddress.com", "ipoo.org", "irish2me.net", "isgreat.org", "itspartytime.co",
    "je-suis-une-poubelle.fr", "jetable.net", "jnxjn.com", "junk1e.com", "junkmail.ga",
    "junkmail.gq", "klzlk.com", "kurzepost.de", "laste.ml", "lazyinbox.com", "letthemeatspam.com",
    "lhsdv.com", "lifebyfood.com", "link2mail.net", "litedrop.com", "lol.ovh", "lookugly.com",
    "lr78.com", "m-c.cc", "mail-temporaire.fr", "mail-tester.com", "mail4trash.com",
    "mailbidon.com", "mailcatch.net", "maildecheterie.com", "maildrop.cf", "maildrop.ga",
    "maildrop.gq", "maildrop.ml", "maildrop.org", "maileater.com", "mailexpire.com",
    "mailforspam.com", "mailimate.com", "mailinblack.com", "mailinator2.com", "mailismagic.com",
    "mailjunk.org", "mailme.org", "mailmoat.com", "mailnes.com", "mailnew.com", "mailnull.de",
    "mailnull.net", "mailnull.org", "mailperdu.fr", "mailpick.biz", "mailquack.com",
    "mailscrap.com", "mailslite.com", "mailslurp.com", "mailtemp.info", "mailtothis.com",
    "mailtrash.net", "mailzi.ru", "meltmail.com", "messagebeamer.de", "misterpinball.de",
    "moncourrier.fr.nf", "monemail.fr.nf", "monmail.fr.nf", "motherearth.com", "msgsafe.io",
    "mug.org", "mycleaninbox.com", "myinbox.net", "myspamfreeemail.com", "mytempemail.com",
    "mytrashmail.com", "nagking.com", "neomailbox.com", "netcourrier.com", "nobulk.com",
    "noclickemail.com", "nomail.xl.cx", "nospam.ze.tc", "nospam4.us", "nospamfor.us",
    "nospammail.net", "notsharingmy.info", "nowmymail.com", "nullbox.org", "nurfuerspam.de",
    "nwldx.com", "objectmail.com", "oneoffmail.com", "onewaymail.com", "online.ms",
    "oopi.org", "otherinbox.com", "ourklips.com", "outlawthru.com", "owlymail.com",
    "pancakemail.com", "pookmail.com", "privacy.net", "proxymail.eu", "pubmail.net",
    "quickinbox.com", "rcpt.at", "recode.me", "redchan.it", "regbypass.com", "rejectmail.com",
    "rmqkr.net", "safetymail.info", "safetypost.de", "sandvikens.se", "saynotospams.com",
    "schafmail.de", "schrottmail.ch", "schrottmail.de", "scrapmail.com", "secupost.net",
    "sendfreeemail.org", "sendspamhere.com", "sharedmailbox.org", "shitmail.de", "shitmail.me",
    "shitmail.org", "shortmail.net", "sinnlos-mail.de", "slaskpost.se", "slopsbox.com",
    "smashmail.de", "sneakemail.com", "sofort-mail.de", "sogetthis.com", "soodonims.com",
    "spamavert.com", "spambob.com", "spambob.net", "spambob.org", "spambox.info",
    "spambox.us", "spamcannibal.org", "spamcon.org", "spamday.com", "spameater.com",
    "spameater.org", "spamfree24.org", "spamfreeemail.com", "spamgoes.in", "spamhole.com",
    "spamify.com", "spaminator.de", "spamkill.info", "spammotel.com", "spammustdie.com",
    "spamoff.de", "spampal.org", "spamprefix.com", "spamshell.com", "spamspot.com",
    "spamstack.net", "spamthisplease.com", "speed.1s.fr", "superstachel.de", "suremail.org",
    "tafmail.com", "teewars.org", "teleworm.com", "tempamail.com", "tempemail.biz",
    "tempemail.net", "tempinbox.co.uk", "tempinbox.com", "tempmail.de", "tempmail2.com",
    "tempmailer.com", "tempmailer.de", "temporaryemail.net", "temporaryforwarding.com",
    "temporaryinbox.com", "throwawayemailaddress.com", "tittbit.in", "trash-attac.de",
    "trash-mail.at", "trash-mail.ch", "trashbox.eu", "trashcanmail.com", "trashmailer.com",
    "trashymail.com", "tvpost.net", "uggsrock.com", "upliftnow.com", "valideur.com",
    "venompen.com", "verwegwerfadresse.de", "vgxmail.com", "voidmail.net", "walala.org",
    "weg-mit-dem-spam.de", "wegwerf-email.org", "wegwerfadresse.net", "wegwerfmail.de",
    "wegwerfmail.net", "wegwerfmail.org", "wetrainbayarea.com", "whyspam.me", "willselfdestruct.com",
    "winemaven.in", "wuzup.net", "xagloo.com", "xemaps.com", "xents.com", "xmaily.com",
    "yapped.net", "yopmail.net", "youpymail.com", "ytrewq.org", "zeroe.ml", "zippymail.info"
}

def is_disposable_domain(domain: str) -> bool:
    """Vérifie si un domaine est reconnu comme adresse jetable."""
    d = domain.lower().strip()
    if d in DISPOSABLE_DOMAINS:
        return True
    
    # Détection par heuristique sur les sous-domaines (ex: *.yopmail.com, *.mailinator.com)
    for root in ("yopmail.", "mailinator.", "trashmail.", "guerrillamail.", "temp-mail.", "tempmail."):
        if root in d:
            return True
            
    return False
