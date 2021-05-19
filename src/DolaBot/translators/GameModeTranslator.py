from typing import Optional, Dict, Callable


class GameModeTranslator:
    fn_lookup: Dict[str, Callable[[], str]]

    def __init__(self):
        self.fn_lookup = {}
        for fn in dir(GameModeTranslator):
            if fn.startswith('translate_'):
                # Add the whole mode name
                name = fn.rpartition('translate_')[2]
                self.fn_lookup[name.replace('_', '')] = getattr(self, fn)

                # But also break up the stage into its individual words, so we can be lazy in searching
                # e.g. match 'splat' and 'zones' to translate_splat_zones
                single_word_names = name.split('_')
                for single_name in single_word_names:
                    self.fn_lookup[single_name] = getattr(self, fn)

        # Remove battle -- it's of no use to us.
        self.fn_lookup.pop('battle')

        # Add in common abbreviations
        self.fn_lookup['cb'] = GameModeTranslator.translate_clam_blitz
        self.fn_lookup['rm'] = GameModeTranslator.translate_rainmaker
        self.fn_lookup['sr'] = GameModeTranslator.translate_salmon_run
        self.fn_lookup['sz'] = GameModeTranslator.translate_splat_zones
        self.fn_lookup['tc'] = GameModeTranslator.translate_tower_control

    @staticmethod
    def translate_regular_battle():
        return """\
:flag_gb: Regular Battle
:flag_fr: Match classique
:flag_de: Standard-kampf	
:flag_es: Combate amistoso
:flag_it: Partita amichevole
:flag_nl: Standaardgevecht
:flag_jp: レギュラーマッチ (Regyurā Macchi)
:flag_ru: Бой салаг (Boy salag)
<https://splatoonwiki.org/wiki/Regular_Battle>
"""

    @staticmethod
    def translate_ranked_battle():
        return """\
:flag_gb: Ranked Battle
:flag_fr: Match pro
:flag_de: Rangkampf
:flag_es: Combate competitivo
:flag_it: Partita pro
:flag_nl: Profgevecht
:flag_jp: ガチマッチ (Gachi Matchi)
:flag_ru: Бой элиты (Boy elity)
<https://splatoonwiki.org/wiki/Ranked_Battle>
"""

    @staticmethod
    def translate_squad_battle():
        return """\
:flag_gb: Squad Battle
:flag_fr: Match en groupe
:flag_de: Teamkampf
:flag_es: Combate en equipo
:flag_it: Partita di gruppo
:flag_jp: タッグマッチ (Taggu Macchi)
<https://splatoonwiki.org/wiki/Squad_Battle>
"""

    @staticmethod
    def translate_league_battle():
        return """\
:flag_gb: League Battle
:flag_fr: Match de ligue
:flag_de: Ligakampf
:flag_es: Torneo / Combate de liga
:flag_it: Partita di lega
:flag_nl: Toernooigevecht
:flag_jp: リーグマッチ (rīgu macchi)
:flag_ru: Бой лиги (Boy ligi)
<https://splatoonwiki.org/wiki/League_Battle>
"""

    @staticmethod
    def translate_splatfest_battle():
        return """\
:flag_gb: Splatfest
:flag_fr: Festival
:flag_de: Splatfest
:flag_es: Festival temático / Festival del Teñido
:flag_it: Festival
:flag_nl: Splatfest
:flag_jp: フェス (Fesu)
:flag_ru: Сплатфест (Splatfest)
<https://splatoonwiki.org/wiki/Splatfest>
"""

    @staticmethod
    def translate_private_battle():
        return """\
:flag_gb: Private Battle
:flag_fr: Match privé
:flag_de: Privater Kampf
:flag_es: Combate privado
:flag_it: Privata privata
:flag_nl: Privégevecht
:flag_jp: プライベートマッチ (puraibēto macchi)
:flag_ru: Частный бой
<https://splatoonwiki.org/wiki/Private_Battle>
"""

    @staticmethod
    def translate_turf_war():
        return """\
:flag_gb: Turf War
:flag_fr: Guerre de territoire
:flag_de: Revierkampf
:flag_es: Territorial
:flag_it: Mischie mollusche
:flag_nl: Grondoorlog
:flag_jp: ナワバリバトル (nawabari batoru)
:flag_ru: Бой за район (Boy za rayon)
<https://splatoonwiki.org/wiki/Turf_War>
"""

    @staticmethod
    def translate_splat_zones():
        return """\
:flag_gb: Splat Zones
:flag_fr: Défense de zone
:flag_de: Herrschaft
:flag_es: Pintazonas
:flag_it: Zona splat
:flag_nl: Spetterzones
:flag_jp: ガチエリア (gachi eria)
:flag_ru: Бой за зоны (Boy za zony)
<https://splatoonwiki.org/wiki/Splat_Zones>
"""

    @staticmethod
    def translate_tower_control():
        return """\
:flag_gb: Tower Control
:flag_fr: Expédition risquée
:flag_de: Turmkommando
:flag_es: Torre / Torreón
:flag_it: Torre Mobile
:flag_nl: Torentwist
:flag_jp: ガチヤグラ (gachi yagura)
:flag_ru: Бой за башню (Boy za bashnyu)	
<https://splatoonwiki.org/wiki/Tower_Control>
"""

    @staticmethod
    def translate_rainmaker():
        return """\
:flag_gb: Rainmaker
:flag_fr: Mission Bazookarpe
:flag_de: Operation Goldfisch
:flag_es: Pez dorado
:flag_it: Mission Bazookarp
:flag_nl: Bazookarper
:flag_jp: ガチホコバトル (Gachi hoko Batoru)
:flag_ru: Мегакарп (Megakarp)
<https://splatoonwiki.org/wiki/Rainmaker>
"""

    @staticmethod
    def translate_salmon_run():
        return """\
:flag_gb: Salmon Run
:flag_fr: Salmon Run
:flag_de: Salmon Run
:flag_es: Salmon Run
:flag_it: Salmon Run
:flag_nl: Salmon Run
:flag_jp: サーモンラン (Sāmon ran)
:flag_ru: Salmon Run
<https://splatoonwiki.org/wiki/Salmon_Run>
"""

    @staticmethod
    def translate_clam_blitz():
        return """\
:flag_gb: Clam Blitz
:flag_fr: Pluie de palourdes
:flag_de: Muschelchaos
:flag_es: Asalto Almeja
:flag_it: Vongol gol
:flag_nl: Schelpenstrijd
:flag_jp: ガチアサリ (gachi asari)
:flag_ru: Устробол (Ustrobol)
<https://splatoonwiki.org/wiki/Clam_Blitz>
"""

    @staticmethod
    def translate_the_shoal():
        return """\
:flag_gb: The Shoal
:flag_fr: Calmarcade
:flag_de: Inkcade
:flag_es: El Remolino
:flag_it: Branco
:flag_nl: De Flipper
:flag_jp: イカッチャ (Ikatcha)
:flag_ru: Стайка (Stayka)
<https://splatoonwiki.org/wiki/The_Shoal>
"""

    @staticmethod
    def translate_octo_expansion():
        return """\
:flag_gb: Splatoon 2: Octo Expansion
:flag_fr: Splatoon 2: Octo Expansion
:flag_de: Splatoon 2: Octo Expansion
:flag_es: Splatoon 2: Octo Expansion
:flag_it: Splatoon 2: Octo Expansion
:flag_nl: Splatoon 2: Octo Expansion
:flag_jp: スプラトゥーン2　オクト・エキスパンション (Supuratūn 2 Okuto Ekisupanshon)
:flag_ru: Осьмодополнение (Os'modopolneniye)
<https://splatoonwiki.org/wiki/Octo_Expansion>
"""

    @staticmethod
    def translate_octo_valley():
        return """\
:flag_gb: Octo Valley / Hero Mode
:flag_fr: Octovallée / Mode Héros
:flag_de: Heldenmodus
:flag_es: Valle Pulpo / Modo héroe / Modo Historia
:flag_it: Modalità storia
:flag_nl: Octovallei / Heldenstand
:flag_jp: タコツボバレー (Takotsubo Barē) / ヒーローモード (Hīrō Mōdo)
:flag_ru: Режим «Агент» (Rezhim «Agent»)
<https://splatoonwiki.org/wiki/Octo_Valley_(mode)>
"""

    @staticmethod
    def translate_octo_canyon():
        return """\
:flag_gb: Octo Canyon / Hero Mode
:flag_fr: Mode Héros
:flag_de: Heldenmodus
:flag_es: Cañón Pulpo / Modo héroe / Modo Historia
:flag_it: Modalità storia
:flag_nl: Octocanyon / Verhaalstand
:flag_jp: タコツボキャニオン (Takotsubo Kyanion) / ヒーローモード (Hīrō Mōdo)
:flag_ru: Режим «Агент» (Rezhim «Agent»)
<https://splatoonwiki.org/wiki/Octo_Canyon_(mode)>
"""

    @staticmethod
    def translate_hero_mode():
        return GameModeTranslator.translate_octo_canyon()

    @staticmethod
    def translate_battle_dojo():
        return """\
:flag_gb: Battle Dojo
:flag_fr: Dojo
:flag_es: Arena
:flag_it: Palestra
:flag_jp: バトルドージョー (batoru dōjō)
:flag_ru: Схватка додзё (Skhvatka dodzyo)
<https://splatoonwiki.org/wiki/Battle_Dojo>
"""

    def get_from_query(self, query: str) -> Optional[str]:
        query = query.lower().replace(' ', '').replace('\'', '').replace('-', '')
        matched = self.fn_lookup.get(query, None)
        return matched() if matched else None
