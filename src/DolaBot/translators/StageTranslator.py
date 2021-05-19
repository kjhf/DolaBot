from typing import Optional, Dict, Callable


class StageTranslator:
    fn_lookup: Dict[str, Callable[[], str]]

    def __init__(self):
        self.fn_lookup = {}
        for fn in dir(StageTranslator):
            if fn.startswith('translate_'):
                # Add the whole stage name
                name = fn.rpartition('translate_')[2]
                self.fn_lookup[name.replace('_', '')] = getattr(self, fn)

                # But also break up the stage into its individual words, so we can be lazy in searching
                # e.g. match 'walleye' and 'warehouse' to translate_walleye_warehouse
                single_word_names = name.split('_')
                for single_name in single_word_names:
                    self.fn_lookup[single_name] = getattr(self, fn)

    @staticmethod
    def translate_urchin_underpass():
        return """\
:flag_gb: Urchin Underpass
:flag_fr: Passage Turbot
:flag_de: Dekabahnstation
:flag_es: Parque Viaducto
:flag_it: Periferia Urbana
:flag_pt: Periferia Urbana
:flag_nl: Forelviaduct
:flag_jp: デカライン高架下 (Dekarain Kōkashita)
:flag_ru: Район Дека (Rayon Deka)
:flag_cn: 海星高架下 (Hǎixīng Gāojiàxià)
<https://splatoonwiki.org/wiki/Urchin_Underpass>
"""

    @staticmethod
    def translate_walleye_warehouse():
        return """\
:flag_gb: Walleye Warehouse
:flag_fr: Encrepôt
:flag_de: Kofferfisch-Lager
:flag_es: Almacén Rodaballo
:flag_it: Magazzino 
:flag_nl: Zeeleeuwloods
:flag_jp: ハコフグ倉庫 (hakofugu sōko)
:flag_ru: Инкрабсклад (Inkrabsklad)
<https://splatoonwiki.org/wiki/Walleye_Warehouse>
"""

    @staticmethod
    def translate_saltspray_rig():
        return """\
:flag_gb: Saltspray Rig
:flag_fr: Station Doucebrise / Plate-forme Mouette
:flag_de: Bohrinsel Nautilus
:flag_es: Plataforma Gaviota
:flag_it: Raffineria 
:flag_jp: シオノメ油田 (Shionome Yuden)
<https://splatoonwiki.org/wiki/Saltspray_Rig>
"""

    @staticmethod
    def translate_arowana_mall():
        return """\
:flag_gb: Arowana Mall
:flag_fr: Centre Arowana
:flag_de: Arowana Center
:flag_es: Plazuela del Calamar
:flag_it: Centro commerciale
:flag_pt: Centro comercial Arowana
:flag_nl: Piranha Plaza
:flag_jp: アロワナモール (Arowana Mōru)
:flag_ru: Аравана
<https://splatoonwiki.org/wiki/Arowana_Mall>
"""

    @staticmethod
    def translate_blackbelly_skatepark():
        return """\
:flag_gb: Blackbelly Skatepark
:flag_fr: Skatepark Mako / Plancho Mako
:flag_de: Punkasius-Skatepark
:flag_es: Parque Lubina
:flag_it: Pista Polposkate
:flag_nl: Snoekduik-skatepark
:flag_jp: Ｂバスパーク (Bī Basu Pāku)
:flag_ru: Скейт-парк «Скат» Skeyt-park «Skat»
<https://splatoonwiki.org/wiki/Blackbelly_Skatepark>
"""

    @staticmethod
    def translate_port_mackerel():
        return """\
:flag_gb: Port Mackerel
:flag_fr: Docks Haddock
:flag_de: Heilbutt-Hafen
:flag_es: Puerto Jurel
:flag_it: Porto Polpo
:flag_nl: Hamerhaaihaven
:flag_jp: ホッケふ頭 (Hokke Futō)
:flag_ru: Порт «Корюшка» Port «Koryushka»
<https://splatoonwiki.org/wiki/Port_Mackerel>
"""

    @staticmethod
    def translate_kelp_dome():
        return """\
:flag_gb: Kelp Dome
:flag_fr: Serre Goémon
:flag_de: Tümmlerkuppel
:flag_es: Jardín botánico
:flag_it: Serra di alghe
:flag_nl: Kelpwierkas
:flag_jp: モズク農園 (Mozuku Nōen)
:flag_ru: Ферма ламинарии
<https://splatoonwiki.org/wiki/Kelp_Dome>
"""

    @staticmethod
    def translate_bluefin_depot():
        return """\
:flag_gb: Bluefin Depot
:flag_fr: Mine Marine / Ruines marines
:flag_de: Blauflossen-Depot
:flag_es: Mina costera
:flag_it: Molo Mollusco
:flag_jp: ネギトロ炭鉱 (Negitoro Tankō)
<https://splatoonwiki.org/wiki/Bluefin Depot>
"""

    @staticmethod
    def translate_moray_towers():
        return """\
:flag_gb: Moray Towers
:flag_fr: Tours Girelle
:flag_de: Muränentürme
:flag_es: Torres Merluza
:flag_it: Torri cittadine
:flag_nl: Tonijntorens
:flag_jp: タチウオパーキング (Tachiuo Pākingu)
:flag_ru: Муренские башни
:flag_cn: 带鱼双塔 (Dàiyú shuāng tǎ)
<https://splatoonwiki.org/wiki/Moray_Towers>
"""

    @staticmethod
    def translate_camp_triggerfish():
        return """\
:flag_gb: Camp Triggerfish
:flag_fr: Hippo-Camping
:flag_de: Camp Schützenfisch
:flag_es: Campamento Arowana
:flag_it: Campeggio Totan
:flag_nl: Kamp Karper
:flag_jp: モンガラキャンプ場 (mongara kyanpujō)
:flag_ru: База «Спинорог» Baza «Spinorog»
<https://splatoonwiki.org/wiki/Camp_Triggerfish>
"""

    @staticmethod
    def translate_flounder_heights():
        return """\
:flag_gb: Flounder Heights
:flag_fr: Lotissement Filament / Appartements Filament
:flag_de: Schollensiedlung
:flag_es: Complejo Medusa
:flag_it: Cime sogliolose
:flag_jp: ヒラメが丘団地 (Hirame'ga'oka Danchi)
<https://splatoonwiki.org/wiki/Flounder_Heights>
"""

    @staticmethod
    def translate_hammerhead_bridge():
        return """\
:flag_gb: Hammerhead Bridge
:flag_fr: Pont Esturgeon
:flag_de: Makrelenbrücke
:flag_es: Puente Salmón
:flag_it: Ponte Sgombro
:flag_jp: マサバ海峡大橋 (Masaba Kaikyō Ōhashi)
<https://splatoonwiki.org/wiki/Hammerhead_Bridge>
"""

    @staticmethod
    def translate_museum_dalfonsino():
        return """\
:flag_gb: Museum d'Alfonsino
:flag_fr: Galeries Guppy
:flag_de: Pinakoithek
:flag_es: Museo del Pargo
:flag_it: Museo di Cefalò
:flag_jp: キンメダイ美術館 (Kinmedai Bijutsukan)
<https://splatoonwiki.org/wiki/Museum_d%27Alfonsino>
"""

    @staticmethod
    def translate_mahi_mahi_resort():
        return """\
:flag_gb: Mahi-Mahi Resort
:flag_fr: Club Ca$halot / Spa C-ta-C
:flag_de: Mahi-Mahi-Resort
:flag_es: Spa Cala Bacalao
:flag_it: Villanguilla
:flag_jp: マヒマヒリゾート＆スパ (Mahimahi Rizōto ando Supa)
<https://splatoonwiki.org/wiki/Mahi-Mahi_Resort>
"""

    @staticmethod
    def translate_piranha_pit():
        return """\
:flag_gb: Piranha Pit
:flag_fr: Carrières Caviar
:flag_de: Steinköhler-Grube
:flag_es: Cantera Tintorera
:flag_it: Miniera d'Orata
:flag_jp: ショッツル鉱山 (Shottsuru Kōzan)
:flag_ru: Пираньев карьер (Piran'yev kar'yer)
<https://splatoonwiki.org/wiki/Piranha_Pit>
"""

    @staticmethod
    def translate_ancho_v_games():
        return """\
:flag_gb: Ancho-V Games
:flag_fr: Tentatec Studio
:flag_de: Anchobit Games HQ
:flag_es: Estudios Esturión
:flag_it: Acciugames
:flag_jp: アンチョビットゲームズ (Anchobitto Gēmuzu)
:flag_ru: Гуппи-Геймдев (Guppi-Geymdev)
<https://splatoonwiki.org/wiki/Ancho-V_Games>
"""

    @staticmethod
    def translate_the_reef():
        return """\
:flag_gb: The Reef
:flag_fr: Allées salées
:flag_de: Korallenviertel
:flag_es: Barrio Congrio
:flag_it: Rione Storione
:flag_nl: Sushistraat
:flag_jp: バッテラストリート (battera sutorīto)
:flag_ru: Риф (Rif)
<https://splatoonwiki.org/wiki/The_Reef>
"""

    @staticmethod
    def translate_musselforge_fitness():
        return """\
:flag_gb: Musselforge Fitness
:flag_fr: Gymnase Ancrage
:flag_de: Molluskelbude
:flag_es: Gimnasio Mejillón
:flag_it: Centro polpisportivo
:flag_nl: Vinvis Fitness
:flag_jp: フジツボスポーツクラブ (fujitsubo supōtsu kurabu)
:flag_ru: Спортзал «Кревед!» Sportzal «Kreved!»
<https://splatoonwiki.org/wiki/Musselforge_Fitness>
"""

    @staticmethod
    def translate_starfish_mainstage():
        return """\
:flag_gb: Starfish Mainstage
:flag_fr: Scène Sirène
:flag_de: Seeigel-Rockbühne
:flag_es: Auditorio Erizo
:flag_it: Palco Plancton
:flag_nl: Zeesterrenstage
:flag_jp: ガンガゼ野外音楽堂 (Gangaze Yagai Ongaku-dō)
:flag_ru: КЗ «Иглокожий» KZ «Iglokozhiy»
<https://splatoonwiki.org/wiki/Starfish_Mainstage>
"""

    @staticmethod
    def translate_humpback_pump_track():
        return """\
:flag_gb: Humpback Pump Track
:flag_fr: Piste Méroule
:flag_de: Buckelwal-Piste
:flag_es: Tiburódromo
:flag_it: Tintodromo Montecarpa
:flag_nl: Lekkerbektrack
:flag_jp: コンブトラック(kombu torakku)
:flag_ru: Велозал «9-й вал» Velozal «9-y val»
<https://splatoonwiki.org/wiki/Humpback_Pump_Track>
"""

    @staticmethod
    def translate_inkblot_art_academy():
        return """\
:flag_gb: Inkblot Art Academy
:flag_fr: Institut Calam'arts
:flag_de: Perlmutt-Akademie
:flag_es: Instituto Coralino
:flag_it: Campus Hippocampus
:flag_nl: Koraalcampus
:flag_jp: 海女美術大学 (Ama Bijutsu Daigaku)
:flag_ru: Академия «Лепота» (Akademiya «Lepota»)
<https://splatoonwiki.org/wiki/Inkblot_Art_Academy>
"""

    @staticmethod
    def translate_sturgeon_shipyard():
        return """\
:flag_gb: Sturgeon Shipyard
:flag_fr: Chantier Narval
:flag_de: Störwerft
:flag_es: Astillero Beluga
:flag_it: Cantiere Pinnenere
:flag_nl: Walruswerf
:flag_jp: チョウザメ造船 (Chōzame Zōsen)
:flag_ru: Осетровые верфи (Osetrovyye verfi)
<https://splatoonwiki.org/wiki/Sturgeon_Shipyard>
"""

    @staticmethod
    def translate_shifty_station():
        return """\
:flag_gb: Shifty Station
:flag_fr: Plateforme polymorphe
:flag_de: Wandelzone
:flag_es: Área mutante
:flag_it: Zona mista
:flag_nl: Wisselwereld
:flag_jp: ミステリーゾーン (misuterī zōn)
:flag_ru: Транстанция (Transtantsiya)
<https://splatoonwiki.org/wiki/Shifty_Station>
"""

    @staticmethod
    def translate_manta_maria():
        return """\
:flag_gb: Manta Maria
:flag_fr: Manta Maria
:flag_de: Manta Maria
:flag_es: Corbeta Corvina
:flag_it: Manta Maria
:flag_nl: Klipvisklipper
:flag_jp: マンタマリア号 (Manta Maria gō)
:flag_ru: Манта Мария (Manta Mariya)
<https://splatoonwiki.org/wiki/Manta_Maria>
"""

    @staticmethod
    def translate_snapper_canal():
        return """\
:flag_gb: Snapper Canal
:flag_fr: Canalamar
:flag_de: Grätenkanal
:flag_es: Canal Cormorán
:flag_it: Canale Cannolicchio
:flag_nl: Moeraalkanaal
:flag_jp: エンガワ河川敷 (engawa kasenjiki)
:flag_ru: Подмостовье (Podmostov'ye)
<https://splatoonwiki.org/wiki/Snapper_Canal>
"""

    @staticmethod
    def translate_makomart():
        return """\
:flag_gb: MakoMart
:flag_fr: Supermarché Cétacé
:flag_de: Cetacea-Markt
:flag_es: Ultramarinos Orca
:flag_it: Mercatotano
:flag_nl: Bultrugbazaar
:flag_jp: ザトウマーケット (zatō māketto)
:flag_ru: Горбуша-Маркет (Gorbusha-Market)
<https://splatoonwiki.org/wiki/MakoMart>
"""

    @staticmethod
    def translate_shellendorf_institute():
        return """\
:flag_gb: Shellendorf Institute
:flag_fr: Galerie des Abysses
:flag_de: Abyssal-Museum
:flag_es: Galería Raspa
:flag_it: Museo paleontonnologico
:flag_nl: Vistorisch museum
:flag_jp: デボン海洋博物館 (debon kaiyō hakubutsukan)
:flag_ru: музей «Мезозой» (Muzey "Mezozoy")
<https://splatoonwiki.org/wiki/Shellendorf_Institute>
"""

    @staticmethod
    def translate_goby_arena():
        return """\
:flag_gb: Goby Arena
:flag_fr: Stade Bernique
:flag_de: Backfisch-Stadion
:flag_es: Estadio Ajolote
:flag_it: Arena Sardina
:flag_nl: Planktonstadion
:flag_jp: アジフライスタジアム (Ajifurai Sutajiamu)
:flag_ru: Арена «Лужа» (Arena «Luzha»)
<https://splatoonwiki.org/wiki/Goby_Arena>
"""

    @staticmethod
    def translate_wahoo_world():
        return """\
:flag_gb: Wahoo World
:flag_fr: Parc Carapince
:flag_de: Flunder-Funpark
:flag_es: Pirañalandia
:flag_it: Soglioland
:flag_nl: Waterwonderland
:flag_jp: スメーシーワールド (Sumēshī wārudo)	
:flag_ru: Луна-парк «Язь» (Luna-park "Yaz")
<https://splatoonwiki.org/wiki/Wahoo_World>
"""

    @staticmethod
    def translate_new_albacore_hotel():
        return """\
:flag_gb: New Albacore Hotel
:flag_fr: Hôtel Atoll
:flag_de: Hotel Neothun
:flag_es: Gran Hotel Caviar
:flag_it: Hotel Tellina
:flag_nl: Hotel de Keizersvis
:flag_jp: ホテルニューオートロ (hoteru nyū ōtoro)
:flag_ru: Отель «Прибой» (Otel' "Priboy")
<https://splatoonwiki.org/wiki/New_Albacore_Hotel>
"""

    @staticmethod
    def translate_skipper_pavilion():
        return """\
:flag_gb: Skipper Pavilion
:flag_fr: Lagune aux gobies
:flag_de: Grundel-Pavillon
:flag_es: Puerta del Gobio
:flag_it: Padiglione Capitone
:flag_nl: Palingpaviljoen
:flag_jp: ムツゴ楼 (Mutsugo Rō)
:flag_ru: Парк «Во Сток» (Park «Vo Stok»)
<https://splatoonwiki.org/wiki/Skipper_Pavilion>
"""

    def get_from_query(self, query: str) -> Optional[str]:
        query = query.lower().replace(' ', '').replace('\'', '').replace('-', '')
        matched = self.fn_lookup.get(query, None)
        return matched() if matched else None
