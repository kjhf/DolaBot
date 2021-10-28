import random
import re
from typing import Optional

#: WEAPONS keyed by the actual name, values are "additional" names after spaces and punctuation ('-.) have been removed.
#: e.g. ".52 Gal" already matches ".52gal" and "52gal".
WEAPONS = {
    ".52 Gal": ["gal", "52", "v52", "52g"],  # default gal
    ".52 Gal Deco": ["galdeco", "52deco", "52galdeco", "52gd"],
    ".96 Gal": ["96", "v96", "96g"],
    ".96 Gal Deco": ["96deco", "96galdeco", "96gd"],
    "Aerospray MG": ["mg", "aeromg", "silveraero", "silveraerospray", "aero", "aerospray"],  # default aero
    "Aerospray PG": ["pg", "aeropg", "bronzeaero", "bronzeaerospray"],
    "Aerospray RG": ["rg", "aerorg", "goldaero", "goldaerospray"],
    "Ballpoint Splatling": ["ballpoint", "bp", "pen"],  # default ballpoint
    "Ballpoint Splatling Nouveau": ["ballpointnouveau", "bpn", "bpsn", "bsn"],
    "Bamboozler 14 Mk I": ["bambooi", "bamboo1", "bamboo14mki", "bamboomki", "bamboomk1"],
    "Bamboozler 14 Mk II": ["bambooii", "bamboo2", "bamboo14mkii", "bamboomkii", "bamboomk2"],
    "Bamboozler 14 Mk III": ["bambooiii", "bamboo3", "bamboo14mkiii", "bamboomkiii", "bamboomk3"],
    "Blaster": ["vblaster"],
    "Bloblobber": ["blob", "vblob"],
    "Bloblobber Deco": ["blobdeco"],
    "Carbon Roller": ["carbon", "vcarbon"],
    "Carbon Roller Deco": ["carbondeco", "crd"],
    "Cherry H-3 Nozzlenose": ["cherry", "ch3", "ch3n", "cherrynozzle"],
    "Clash Blaster": ["clash", "vclash", "clashter"],
    "Clash Blaster Neo": ["clashneo", "clashterneo", "cbn"],
    "Classic Squiffer": ["csquif", "csquiff", "bluesquif", "bluesquiff", "squif", "squiff", "squiffer"],  # default squiffer
    "Clear Dapple Dualies": ["cdapple", "cdapples", "cleardualies", "clapples", "clappies", "cdd"],
    "Custom Blaster": ["cblaster"],
    "Custom Dualie Squelchers": ["cds", "customdualies", "cdualies"],
    "Custom E-Liter 4K": ["c4k", "ce4k", "celiter", "celitre", "celiter4k", "celitre4k", "custom4k"],
    "Custom E-Liter 4K Scope": ["c4ks", "ce4ks", "celiterscope", "celitrescope", "celiter4kscope", "celitre4kscope", "custom4kscope"],
    "Custom Explosher": ["cex", "cexplo", "cexplosher"],
    "Custom Goo Tuber": ["customgoo", "cgoo", "cgootube", "cgootuber", "cgt"],
    "Custom Hydra Splatling": ["customhyra", "chydra", "chydrasplatling", "chs"],
    "Custom Jet Squelcher": ["customjet", "cjet", "cjets", "cjs", "cjsquelcher", "cjetsquelcher"],
    "Custom Range Blaster": ["customrange", "crange", "crblaster", "crb"],
    "Custom Splattershot Jr.": ["customjunior", "cjr", "cjnr", "cjunior", "csj"],
    "Dapple Dualies": ["dapples", "vdapples", "vdd", "dd", "ddualies"],
    "Dapple Dualies Nouveau": ["dapplesnouveau", "ddn", "ddualiesn"],
    "Dark Tetra Dualies": ["tetra", "tetras", "tetradualies", "dark", "darks", "darktetra", "darktetras", "darkdualies", "dtd"],  # default tetras
    "Dualie Squelchers": ["ds", "vds"],
    "Dynamo Roller": ["dyna", "dynamo", "vdynamo", "silverdynamo"],
    "E-liter 4K": ["4k", "e4k", "eliter", "elitre", "eliter4k", "elitre4k"],
    "E-liter 4K Scope": ["4ks", "e4ks", "eliterscope", "elitrescope", "eliter4kscope", "elitre4kscope"],
    "Enperry Splat Dualies": ["edualies", "enperries", "enperrydualies", "esd"],
    "Explosher": ["vex", "explo", "vexplo"],
    "Firefin Splat Charger": ["firefin", "firefincharger", "fsc", "ffin"],
    "Firefin Splatterscope": ["firefinscope", "ffinscope"],
    "Flingza Roller": ["fling", "flingza", "vfling", "vflingza"],
    "Foil Flingza Roller": ["foilfling", "foilflingza", "ffling", "fflingza", "ffr"],
    "Foil Squeezer": ["fsqueezer"],
    "Forge Splattershot Pro": ["forge", "forgepro", "fpro", "fsp"],
    "Fresh Squiffer": ["fsquif", "fsquiff", "redsquif", "redsquiff"],
    "Glooga Dualies": ["glooga", "gloogas", "glues", "vglues", "vgloogas", "gd", "vgd"],
    "Glooga Dualies Deco": ["gloogadeco", "gloogasdeco", "gluesdeco", "dglues", "dgloogas", "gdd", "dgd"],
    "Gold Dynamo Roller": ["golddyna", "golddynamo", "gdr"],
    "Goo Tuber": ["goo", "vgoo", "gootube", "vgootube", "vgootuber"],
    "Grim Range Blaster": ["grim", "grange", "grblaster", "grb"],
    "H-3 Nozzlenose": ["h3", "vh3", "h3nozzle", "h3n"],
    "H-3 Nozzlenose D": ["h3d", "h3dnozzle", "h3nd", "h3dn"],
    "Heavy Splatling": ["heavy", "vheavy"],
    "Heavy Splatling Deco": ["heavyd", "heavydeco", "hsd"],
    "Heavy Splatling Remix": ["remix", "heavyremix", "hsr"],
    "Hero Blaster Replica": ["heroblaster"],
    "Hero Brella Replica": ["herobrella"],
    "Hero Charger Replica": ["herocharger"],
    "Hero Dualie Replicas": ["herodualie", "herodualies", "hdualie", "hdualies"],
    "Hero Roller Replica": ["heroroller"],
    "Hero Shot Replica": ["heroshot"],
    "Hero Slosher Replica": ["heroslosh", "heroslosher"],
    "Hero Splatling Replica": ["herosplatling", "heroheavy"],
    "Herobrush Replica": ["herobrush"],
    "Hydra Splatling": ["hydra", "vhydra", "vhydrasplatling"],
    "Inkbrush": ["brush", "vbrush", "vinkbrush"],  # default brush
    "Inkbrush Nouveau": ["brushn", "brushnouveau", "nbrush", "inkbrushn"],
    "Jet Squelcher": ["jet", "vjet", "jets", "vjets", "js", "vjs", "jsquelcher", "vjsquelcher", "vjetsquelcher"],
    "Kensa .52 Gal": ["kgal", "k52", "k52gal"],  # default kgal
    "Kensa Charger": ["kcharger"],
    "Kensa Dynamo Roller": ["kdyna", "kdynamo", "kensadynamo", "kdr"],
    "Kensa Glooga Dualies": ["kensaglooga", "kensagloogas", "kensaglues", "klues", "kglues", "klooga", "kloogas", "kgloogas", "kgd"],
    "Kensa L-3 Nozzlenose": ["knozzle", "kl3", "kl3n", "kl3nozzle"],
    "Kensa Luna Blaster": ["kensaluna", "kluna", "kuna", "kunablaster", "klb"],
    "Kensa Mini Splatling": ["kensamini", "kmini", "kimi", "kimisplatling", "kminisplatling", "kms"],
    "Kensa Octobrush": ["kensabrush", "kbrush", "krush", "kocto", "koctobrush", "kob"],
    "Kensa Rapid Blaster": ["kensarapid", "krapid", "krapidblaster", "kraster", "krb"],
    "Kensa Sloshing Machine": ["kensasloshmachine", "ksloshmachine", "kensamachine", "kmachine", "kachine", "kachin", "ksm"],
    "Kensa Splat Dualies": ["kensadualie", "kensadualies", "kdaulies", "kdaulie", "kdualie", "kdualies", "kaulies", "kualies", "kaulie", "kualie", "ksd"],
    "Kensa Splat Roller": ["kensaroller", "kroller", "kroll", "ksr"],
    "Kensa Splatterscope": ["kensascope", "ksscope", "kscope", "kss"],
    "Kensa Splattershot": ["kensashot", "ksshot", "kshot"],
    "Kensa Splattershot Jr.": ["kensajunior", "kjr", "kjnr", "kjunior", "ksj"],
    "Kensa Splattershot Pro": ["kensapro", "kpro", "ksp"],
    "Kensa Undercover Brella": ["kensaundercover", "kunder", "kensabrella", "kub"],
    "Krak-On Splat Roller": ["krakon", "krakonroller", "krack", "krackonroller", "krak", "krakenroller", "koroller", "koro", "kosr"],
    "L-3 Nozzlenose": ["l3", "vl3", "l3nozzle", "l3n"],
    "L-3 Nozzlenose D": ["l3d", "l3dnozzle", "l3nd", "l3dn"],
    "Light Tetra Dualies": ["light", "lights", "lightdualies", "lighttetra", "lighttetras"],
    "Luna Blaster": ["luna", "vluna", "vuna", "vlunablaster"],
    "Luna Blaster Neo": ["lunaneo", "lbn"],
    "Mini Splatling": ["mini", "vmini", "vimi", "vimisplatling", "vminisplatling", "vms"],
    "N-ZAP '83": ["zap83", "83", "bronzenzap", "bronzezap", "brownnzap", "brownzap", "rednzap", "redzap"],  # By Twitter poll, this zap is the red one.
    "N-ZAP '85": ["zap85", "85", "greynzap", "greyzap", "graynzap", "grayzap", "zap", "nzap"],  # default zap
    "N-ZAP '89": ["zap89", "89", "orangenzap", "orangezap"],
    "Nautilus 47": ["naut47", "47", "naut"],  # default nautilus
    "Nautilus 79": ["naut79", "79"],
    "Neo Splash-o-matic": ["neosplash", "nsplash", "nsplashomatic"],
    "Neo Sploosh-o-matic": ["neosploosh", "nsploosh", "nsplooshomatic"],
    "New Squiffer": ["nsquif", "nsquiff", "newsquif", "newsquiff"],
    "Octobrush": ["octo", "obrush", "vocto", "voctobrush", "vobrush"],
    "Octobrush Nouveau": ["octon", "obrushn", "octobrushn"],
    "Octo Shot Replica": ["oshot", "osr"],
    "Permanent Inkbrush": ["pbrush", "permabrush", "permanentbrush", "pinkbrush", "permainkbrush"],
    "Range Blaster": ["range", "vrange", "vrangeblaster"],
    "Rapid Blaster": ["rapid", "vrapid", "vrapidblaster"],
    "Rapid Blaster Deco": ["rapiddeco", "rapidd", "rapidblasterd", "rbd"],
    "Rapid Blaster Pro": ["rapidpro", "prorapid", "rbp"],
    "Rapid Blaster Pro Deco": ["rapidprodeco", "prodecorapid", "rbpd"],
    "Slosher": ["slosh", "vslosh"],
    "Slosher Deco": ["sloshd", "sloshdeco"],
    "Sloshing Machine": ["sloshmachine", "vsloshmachine", "vmachine", "machine", "vachine", "vsm"],
    "Sloshing Machine Neo": ["sloshmachineneo", "neosloshmachine", "neomachine", "machineneo", "smn"],
    "Soda Slosher": ["soda", "sodaslosh"],
    "Sorella Brella": ["sorella", "sbrella", "srella"],
    "Splash-o-matic": ["splash", "vsplash", "vsplashomatic"],
    "Splat Brella": ["brella", "vbrella", "vsplatbrella"],
    "Splat Charger": ["charger", "vcharger", "vsplatcharger"],
    "Splat Dualies": ["dualies", "vdualies", "vsplatdualies"],
    "Splat Roller": ["roller", "vroller", "vsplatroller"],
    "Splatterscope": ["scope", "vscope", "vsplatscope", "vsplatterscope"],
    "Splattershot": ["shot", "vshot", "vsplatshot", "vsplattershot"],
    "Splattershot Jr.": ["junior", "jr", "vjr", "jnr", "vjnr", "vjunior", "vsj"],
    "Splattershot Pro": ["pro", "vpro", "vsplatshotpro", "vsplatterpro"],
    "Sploosh-o-matic": ["sploosh", "vsploosh", "vsplooshomatic"],
    "Sploosh-o-matic 7": ["7", "sploosh7", "7sploosh", "7splooshomatic"],
    "Squeezer": ["vsqueezer"],
    "Tenta Brella": ["tent", "vent", "vtent", "tentbrella", "vtentbrella"],
    "Tenta Camo Brella": ["tentcamo", "camo", "camotent", "camobrella", "tentcamobrella", "tcb"],
    "Tenta Sorella Brella": ["tentsorella", "tsorella", "sorellatent", "tsorellabrella", "tentsorellabrella", "tsb"],
    "Tentatek Splattershot": ["ttek", "ttekshot", "tshot", "ttshot", "ttsplatshot", "ttsplattershot", "ttss", "ttk"],
    "Tri-Slosher": ["tri", "trislosh", "vtri", "vtrislosh", "vtrislosher"],
    "Tri-Slosher Nouveau": ["trin", "trisloshn", "trinouveau", "trisloshnouveau", "tsn"],
    "Undercover Brella": ["undercover", "ubrella", "vundercover", "vundercoverbrella"],
    "Undercover Sorella Brella": ["sunder", "sundercover", "undercoversorella", "sundercoverbrella", "usb"],
    "Zink Mini Splatling": ["zinkmini", "zmini", "zimi", "zimisplatling", "zminisplatling", "zms"],
}


def transform_weapon(wep: str) -> str:
    # Lowercase and remove spaces and punctuation
    wep = re.sub(r"[ .\-']", '', wep.lower())

    # Typo corrections
    wep = wep.replace("duel", "dual")
    
    return wep


# Also add in the transformed names of the key.
for w_key in WEAPONS.keys():
    WEAPONS[w_key] = set([transform_weapon(w_key)] + WEAPONS[w_key])


def get_random_weapon() -> str:
    return random.choice(list(WEAPONS.keys()))


def try_find_weapon(search: str, exact: bool = False) -> Optional[str]:
    result = next((w for w in WEAPONS if w == search), None)
    if result or exact:
        return result
    else:
        # Search inexact
        search = transform_weapon(search)

        for key in WEAPONS:
            if any(wep_label == search for wep_label in WEAPONS[key]):
                return key

        return None
