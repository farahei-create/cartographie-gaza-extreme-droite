import json, datetime
N=[];E=[]
def P(id,name,role,desc,st=None,type="person"):
    N.append({"id":id,"name":name,"type":type,"role":role,"description":desc,"statements":[dict(zip(["quote","date","medium","url","theme"],s)) for s in (st or [])]})
def O(id,name,role,desc): P(id,name,role,desc,[],"org")
def L(s,t,rel,url,date): E.append({"source":s,"target":t,"relation":rel,"url":url,"date":date})
G="Gaza – déclarations"; X="Proximité extrême droite"; M="Médias – structure"
# URLs
FI_BERGE="https://www.franceinfo.fr/monde/proche-orient/israel-palestine/denoncer-un-genocide-a-gaza-c-est-une-falsification-historique-estime-la-ministre-chargee-de-la-lutte-contre-les-discriminations-aurore-berge_7392085.html"
HUFF_LEPEN="https://www.huffingtonpost.fr/politique/article/marine-le-pen-soutient-sans-reserve-ce-que-fait-israel-a-gaza_250113.html"
F24_BARDELLA="https://www.france24.com/fr/info-en-continu/20250326-en-isra%C3%ABl-bardella-rencontre-des-survivants-du-7-octobre-et-d%C3%A9fend-un-front-commun"
RMC_BARDELLA="https://rmc.bfmtv.com/actualites/politique/jordan-bardella-en-israel-je-n-y-vais-pas-pour-parler-du-conflit-assure-le-president-du-rn_AV-202503190364.html"
FI_MARECHAL_IL="https://www.franceinfo.fr/politique/marion-marechal-lance-son-propre-mouvement-politique-et-propose-une-coalition-a-marine-le-pen_6824000.html"
FI_MARECHAL_JUIN="https://www.franceinfo.fr/elections/legislatives/elections-legislatives-2024-marion-marechal-deplore-un-changement-de-position-du-rn-qui-refuse-le-principe-d-un-accord-avec-reconquete_6598065.html"
FI_CIOTTI="https://www.franceinfo.fr/politique/legislatives-anticipees-eric-ciotti-dit-oui-a-une-alliance-des-republicains-avec-le-rn_6598017.html"
FI_KLARS="https://www.franceinfo.fr/elections/legislatives/legislatives-l-historien-serge-klarsfeld-votera-pour-le-rassemblement-national-en-cas-de-duel-face-a-la-france-insoumise_6607854.html"
F24_YBP="https://www.france24.com/fr/france/20231022-ya%C3%ABl-braun-pivet-en-isra%C3%ABl-avec-les-faucons-de-lr-un-voyage-qui-s%C3%A8me-le-trouble"
FI_BOLLORE="https://www.franceinfo.fr/economie/medias/canal-i-tele-paris-match-avant-le-jdd-la-mainmise-de-vincent-bollore-sur-d-autres-medias-a-braque-de-nombreuses-redactions_5910392.html"
EU1_ZEM="https://www.europe1.fr/international/israel-hamas-je-ne-suis-pas-daccord-avec-la-treve-humanitaire-explique-eric-zemmour-4211594"
FI_ZEM_CNEWS="https://www.franceinfo.fr/politique/eric-zemmour/presidentielle-cnews-met-fin-aux-chroniques-du-possible-candidat-eric-zemmour-apres-la-decision-du-csa-de-decompter-son-temps-de-parole_4769613.html"
MINUTES_HABIB="https://www.20minutes.fr/justice/4118457-20241029-guerre-israel-hamas-meyer-habib-compare-population-gaza-cancer-enquete-ouverte"
MARIANNE_YADAN="https://www.marianne.net/politique/lrem/la-deputee-caroline-yadan-essaie-t-elle-vraiment-de-faire-interdire-toute-mention-de-genocide-a-gaza"
MINUTES_TORRES="https://www.20minutes.fr/monde/israel/4155846-20250528-gaza-population-augmente-enclave-palestinienne-pourquoi-idee-tient"
FI_ENTH="https://www.franceinfo.fr/monde/proche-orient/israel-palestine/on-vous-explique-la-polemique-autour-de-raphael-enthoven-deprogramme-du-festival-livres-dans-la-boucle-apres-ses-messages-sur-gaza_7480282.html"
STRAT_FT="https://www.strategies.fr/medias/caroline-fourest-directrice-editoriale-et-editorialiste-de-franc-tireur"
SUD_LEVY_BIO="https://www.sudradio.fr/nos-biographies/elisabeth-levy-biographie"
T7J="https://www.programme-television.org/news/people/polemique/pascal-praud-sen-prend-a-nagui-apres-lusage-du-mot-genocide-pour-qualifier-la-guerre-a-gaza-6643"
EU1_CARR="https://www.europe1.fr/international/pascal-praud-et-vous-conflit-israel-hamas-le-mot-genocide-ne-correspond-pas-a-la-realite-estime-gerard-carreyrou-774797"
VP_VALLS="https://www.vie-publique.fr/discours/296889-manuel-valls-16012025-europe-1-israel-hamas-cessez-le-feu-et-mayotte"
F24_MENARD="https://www.france24.com/fr/20140328-municipales-robert-menard-beziers-fn-rsf-liberte-presse-le-pen-mairie"
CNEWS_GOLD="https://www.cnews.fr/videos/monde/2024-10-07/jamais-israel-na-voulu-cibler-un-civil-soutient-gilles-william-goldnadel"
BFM_ARFI="https://www.bfmtv.com/politique/yonathan-arfi-president-du-crif-l-accusation-de-genocide-ne-vise-pas-a-proteger-les-palestiniens-mais-resonne-comme-un-cri-de-ralliement-pour-stigmatiser-les-juifs_VN-202405060963.html"
CNEWS_THOUV="https://www.cnews.fr/monde/2025-08-03/guerre-au-proche-orient-un-genocide-cest-faire-disparaitre-volontairement-un"
CNEWS_MAR="https://www.cnews.fr/monde/2024-05-21/marion-marechal-il-ny-pas-de-genocide-gaza-sinon-il-ny-aurait-pas-des-evacuations"
BFM_CIOTTI="https://www.bfmtv.com/politique/les-republicains/elle-s-est-decredibilisee-eric-ciotti-souhaite-que-la-france-quitte-la-cour-penale-internationale_AV-202405220346.html"
HUFF_FOUREST="https://www.huffingtonpost.fr/politique/article/guerre-israel-hamas-apres-les-propos-de-fourest-sur-les-morts-de-gaza-les-deputes-lfi-saisissent-l-arcom_225122.html"

# ---------- PERSONNES ----------
P("caroline-yadan","Caroline Yadan","Députée (groupe EPR / Renaissance), 8e circonscription des Français établis hors de France",
 "Élue en 2024 dans la circonscription précédemment représentée par Meyer Habib. Autrice d'une proposition de loi (nov. 2024) sur les formes renouvelées de l'antisémitisme, soutenue par Aurore Bergé.",
 [("Qualifier de génocide l'opération menée par Tsahal relève de la manipulation politique qui met en danger les juifs de France","2024-09-09","Le Point (tribune)","https://www.lepoint.fr/debats/qualifier-de-genocide-l-operation-menee-par-l-armee-israelienne-releve-de-la-manipulation-politique-09-09-2024-2569814_2.php",G),
  ("Un génocide ne dépend pas du nombre mais de l'intention.","2024-09-09","Le Point (tribune)","https://www.lepoint.fr/debats/qualifier-de-genocide-l-operation-menee-par-l-armee-israelienne-releve-de-la-manipulation-politique-09-09-2024-2569814_2.php",G),
  ("l'armée israélienne, qui prévient les populations civiles avant les bombardements, ce que, sauf omission de ma part, aucune autre armée au monde ne fait, ne commet aucun massacre.","2024-09-09","Le Point (tribune)","https://www.lepoint.fr/debats/qualifier-de-genocide-l-operation-menee-par-l-armee-israelienne-releve-de-la-manipulation-politique-09-09-2024-2569814_2.php",G),
  ("je n'ai pu, en conscience, laisser parler d'un « génocide » en cours à Gaza […] C'est ce qu'a été la Shoah. Ce n'est pas ce que nous voyons à Gaza.","2025-07-02","LinkedIn (publication de l'intéressée)","https://fr.linkedin.com/posts/caroline-yadan-05259625a_dans-le-cadre-de-lexamen-des-r%C3%A9solutions-activity-7346234799956615168-muNj",G),
  ("[sa proposition de loi] ne vient pas interdire l'emploi du mot génocide (qui n'en est pas un) à Gaza…","2025-07-23","Message sur X, cité par Marianne",MARIANNE_YADAN,G)])
P("aurore-berge","Aurore Bergé","Ministre déléguée chargée de l'Égalité femmes-hommes et de la Lutte contre les discriminations (Renaissance)",
 "Membre du gouvernement. A soutenu la proposition de loi de Caroline Yadan.",
 [("[dénoncer un génocide à Gaza] c'est une falsification historique","2025-07-22","franceinfo",FI_BERGE,G),
  ("on ne peut pas accepter les falsifications historiques","2025-07-22","franceinfo",FI_BERGE,G)])
P("patrick-klugman","Patrick Klugman","Avocat, président du Comité français pour Yad Vashem",
 "Le Comité qu'il préside a publié en juillet 2025 un communiqué sur l'usage du terme « génocide » à propos de Gaza.",
 [("afin que l'abus de l'accusation de génocide puisse entrer dans les cas possibles de contestation de crime contre l'humanité","2025-07-22","Communiqué du Comité français pour Yad Vashem, cité par franceinfo (date de l'article)",FI_BERGE,G)])
P("meyer-habib","Meyer Habib","Ancien député apparenté LR (8e circonscription des Français établis hors de France, jusqu'en 2024)",
 "Ancien député, visé par une enquête ouverte en 2024 après une plainte de la LDH pour des propos tenus sur Radio J ; il affirme que ses propos ont été « sciemment dénaturés ».",
 [("La grande solidarité arabe ! Parce qu'ils savent aujourd'hui le cancer qu'est cette population. A qui on a tout donné. Israël est sorti de la bande de Gaza","2023-10-20","Radio J, cité par 20 Minutes / AFP",MINUTES_HABIB,G),
  ("Mes propos ont été sciemment dénaturés… [il n'a] jamais visé l'ensemble de la population","2024-10-29","Réponse de l'intéressé, citée par 20 Minutes",MINUTES_HABIB,G),
  ("Son discours est irréprochable, à la différence de celui d'Emmanuel Macron et de ses amis","2025-05-15","i24NEWS, cité par Le HuffPost (à propos de Marine Le Pen)",HUFF_LEPEN,X)])
P("marine-le-pen","Marine Le Pen","Présidente du groupe RN à l'Assemblée nationale, députée du Pas-de-Calais",
 "Figure principale du Rassemblement national.",
 [("[Israël] fait ce qu'il peut dans une situation extrêmement difficile","2025-05-15","i24NEWS, cité par Le HuffPost",HUFF_LEPEN,G),
  ("Quand Israël veut déplacer des populations, on lui dit que c'est horrible et honteux. Mais j'imagine que ces déplacements servent à éradiquer le Hamas sans avoir une population civile qui sert de bouclier","2025-05-15","i24NEWS, cité par Le HuffPost",HUFF_LEPEN,G),
  ("Israël ne refuse pas de livrer de l'alimentation et des biens de première nécessité à Gaza, il ne veut simplement pas que ce soit le Hamas qui les distribue","2025-05-15","i24NEWS, cité par Le HuffPost",HUFF_LEPEN,G)])
P("jordan-bardella","Jordan Bardella","Président du Rassemblement national",
 "S'est rendu en Israël en mars 2025 à l'invitation du ministre israélien Amichai Chikli pour une conférence sur l'antisémitisme.",
 [("la civilisation contre la barbarie","2025-03-26","AFP, cité par France 24",F24_BARDELLA,G),
  ("Je n'y vais pas pour commenter les opérations militaires","2025-03-19","RMC",RMC_BARDELLA,G)])
P("marion-marechal","Marion Maréchal","Députée européenne, fondatrice d'Identité-Libertés (ex-vice-présidente de Reconquête)",
 "Tête de liste Reconquête aux européennes 2024, exclue du parti après avoir appelé à une alliance avec le RN ; a lancé Identité-Libertés en octobre 2024 pour une « coalition » avec Marine Le Pen, Jordan Bardella et Éric Ciotti.",
 [("Il n'y a pas de génocide à Gaza, sinon il n'y aurait pas des évacuations de population ou la livraison de matériels humanitaires","2024-05-21","CNews",CNEWS_MAR,G),
  ("J'ai décidé de lancer un mouvement politique pour contribuer à la victoire du camp national","2024-10-07","Le Figaro, cité par franceinfo",FI_MARECHAL_IL,X)])
P("eric-zemmour","Éric Zemmour","Président de Reconquête",
 "Ancien chroniqueur de « Face à l'info » sur CNews jusqu'en septembre 2021, candidat à la présidentielle 2022.",
 [("L'important pour Israël est de rétablir son rapport de force, quel que soit le cas. Et ce, peu importe le prix","2023-10-29","Le Grand Rendez-Vous Europe 1 / CNews / Les Echos",EU1_ZEM,G),
  ("Une vie vaut une vie","2023-10-29","Le Grand Rendez-Vous Europe 1 / CNews / Les Echos",EU1_ZEM,G),
  ("Donc non, je ne suis pas d'accord avec la trêve humanitaire","2023-10-29","Le Grand Rendez-Vous Europe 1 / CNews / Les Echos",EU1_ZEM,G)])
P("eric-ciotti","Éric Ciotti","Député, ancien président des Républicains",
 "A annoncé le 11 juin 2024, alors président de LR, une alliance avec le RN pour les législatives anticipées.",
 [("La Cour pénale internationale s'est définitivement décrédibilisée, elle n'existera plus","2024-05-22","BFMTV",BFM_CIOTTI,G),
  ("Il faut une alliance, c'est le sens de la cinquième République","2024-06-11","TF1, cité par franceinfo",FI_CIOTTI,X),
  ("Serge Klarsfeld ne se trompe pas d'ennemi !","2024-06-16","Message sur X, cité par franceinfo",FI_KLARS,X)])
P("yael-braun-pivet","Yaël Braun-Pivet","Présidente de l'Assemblée nationale (Renaissance)",
 "S'est rendue en Israël les 21-22 octobre 2023 avec Éric Ciotti, Meyer Habib et Mathieu Lefèvre. A reconnu en avril 2025 avoir eu « tort » d'employer le mot « inconditionnel ».",
 [("Ce qui est important, c'est que les populations civiles qui se trouvent à Gaza soient le moins possible victimes de ce conflit. Mais on sait aussi qu'elles servent souvent de bouclier humain. Il faut les préserver bien sûr, mais rien ne doit empêcher Israël de se défendre. Il y a un attaquant et des attaqués","2023-10-22","Déclaration en Israël, citée par France 24",F24_YBP,G),
  ("Je vois bien que j'ai eu tort de choisir ce mot, parce qu'il ne reflétait pas ma pensée et il a été compris de telle sorte que ça ne correspond pas à ce que je voulais dire","2025-04-10","France Inter, cité par BFMTV","https://www.bfmtv.com/politique/parlement/soutien-inconditionnel-a-israel-yael-braun-pivet-reconnait-avoir-eu-tort-de-choisir-ce-mot_AD-202504100354.html","Nuance / contexte")])
P("robert-menard","Robert Ménard","Maire de Béziers",
 "Élu maire de Béziers en 2014 avec le soutien du Front national. Qualifie la situation à Gaza de « massacre » tout en récusant le terme de génocide.",
 [("Non, ce n'est pas un génocide qui se passe à Gaza. Un génocide, c'est la volonté affichée de détruire un peuple","2025-05-22","RTL","https://www.rtl.fr/actu/international/une-ignominie-robert-menard-tance-eric-coquerel-sur-rtl-et-refute-le-terme-de-genocide-a-gaza-7900507815",G),
  ("C'est un massacre, c'est quelque chose de terrible, mais c'est pas un génocide","2025-05-22","RTL","https://www.rtl.fr/actu/international/une-ignominie-robert-menard-tance-eric-coquerel-sur-rtl-et-refute-le-terme-de-genocide-a-gaza-7900507815",G)])
P("manuel-valls","Manuel Valls","Ancien Premier ministre",
 "A accompagné une délégation de parlementaires en Israël en octobre 2023. Déclare par ailleurs combattre le Rassemblement national.",
 [("La responsabilité de cette guerre, avec ses morts, ses victimes, ses souffrances, elle incombe d'abord et avant tout au Hamas.","2025-01-16","Europe 1 / CNews (transcription vie-publique.fr)",VP_VALLS,G),
  ("je combats le Rassemblement National","2025-01-16","Europe 1 / CNews (transcription vie-publique.fr)",VP_VALLS,"Nuance / contexte")])
P("bernard-henri-levy","Bernard-Henri Lévy","Philosophe, essayiste, chroniqueur au Point",
 "Auteur de « Solitude d'Israël » (2024). A annulé sa participation à la conférence de Jérusalem de mars 2025 en raison de l'invitation de Jordan Bardella, et s'est dit méfiant à l'égard du soutien de l'extrême droite.",
 [("Israël fait tout ce qu'il peut pour qu'il y ait le moins possible de victimes civiles. Il n'y a pas de génocide à Gaza, il n'y a pas de massacre délibéré des populations civiles à Gaza, tout cela est faux.","2024-04-02","France 3 Côte d'Azur (entretien publié le 04/04/2024)","https://france3-regions.franceinfo.fr/provence-alpes-cote-d-azur/alpes-maritimes/nice/entretien-bernard-henri-levy-il-n-y-a-pas-de-genocide-a-gaza-il-n-y-a-pas-de-massacre-delibere-des-populations-civiles-2949686.html",G),
  ("Eh oui. Je le répéterai sur tous les tons s'il le faut. Il n'y a pas de genocide à Gaza.","2026-10-15","X (@BHL)","https://x.com/BHL/status/2110817601270231314",G),
  ("Et l'extrême droite qui nous dit qu'elle s'est convertie, qu'elle était antisémite, qu'elle ne l'est plus, quelle merveille si c'est vrai. Mais si c'est vrai : il faut des preuves.","2024-04-02","France 3 Côte d'Azur","https://france3-regions.franceinfo.fr/provence-alpes-cote-d-azur/alpes-maritimes/nice/entretien-bernard-henri-levy-il-n-y-a-pas-de-genocide-a-gaza-il-n-y-a-pas-de-massacre-delibere-des-populations-civiles-2949686.html","Nuance / contexte")])
P("raphael-enthoven","Raphaël Enthoven","Philosophe, membre du comité de rédaction de Franc-Tireur",
 "Déprogrammé du festival « Livres dans la boucle » en 2025 après des messages sur X concernant les journalistes à Gaza. A publiquement corrigé une affirmation chiffrée en octobre 2026.",
 [("Il n'y a AUCUN journaliste à Gaza. Uniquement des tueurs, des combattants ou des preneurs d'otages avec une carte de presse.","2025-08-15","X, cité par franceinfo",FI_ENTH,G),
  ("Je persiste. A mon sens, il n'y a aucun journaliste à Gaza, car je refuse la qualité de journaliste à quiconque travaille pour une organisation terroriste.","2025-08-17","X, cité par franceinfo",FI_ENTH,G),
  ("Je n'en peux plus, de ce \"génocide\" commis par une nation agressée sur une population qui a augmenté depuis le début des combats, […]","2026-10-10","X (@Enthoven_R)","https://x.com/Enthoven_R/status/2108828983693373510",G),
  ("J'ai tort sur un point. La population de Gaza n'a pas augmenté, mais légèrement diminué en valeur absolue depuis le 7 octobre 2023. Mais ça ne change rien sur le fond. Une guerre n'est pas un génocide.","2026-10-11","X (@Enthoven_R)","https://x.com/Enthoven_R/status/2109306896901361749",G),
  ("il propage le mythe du « génocide à Gaza » dont la raison d'être est de rendre digeste le 7 octobre en lui opposant un crime encore plus grave.","2026-10-07","X (@Enthoven_R)","https://x.com/Enthoven_R/status/2107851573879832611",G)])
P("caroline-fourest","Caroline Fourest","Journaliste, essayiste, directrice éditoriale de Franc-Tireur",
 "Ses propos sur BFMTV en octobre 2023 ont conduit des députés LFI à saisir l'Arcom ; elle a maintenu sa position tout en qualifiant de « grave » la mort d'innocents.",
 [("on ne peut pas comparer le fait d'avoir tué des enfants délibérément comme le Hamas, et le fait de les tuer involontairement comme Israël","2023-10-29","BFMTV, cité par Le HuffPost",HUFF_FOUREST,G),
  ("Je maintiens, malgré la meute, qu'il existe une différence d'intention fondamentale entre cibler des enfants pour les décapiter et perdre la tête au point de bombarder le Hamas au milieu d'enfants. Comme je maintiens que c'est grave et tuer des innocents.","2023-10-30","X, cité par Le HuffPost",HUFF_FOUREST,G)])
P("gilles-william-goldnadel","Gilles-William Goldnadel","Avocat, essayiste, chroniqueur sur CNews et au Figaro, président d'Avocats sans frontières",
 "Intervient régulièrement sur CNews et Europe 1.",
 [("Jamais Israël n'a voulu cibler un civil","2024-10-07","CNews",CNEWS_GOLD,G),
  ("il n'y a pas de génocide à Gaza. Il n'y a aucun élément juridique, aucun jugement qui a vu un génocide.","2025-10-01","« Pascal Praud et vous » (Europe 1 / CNews), cité par Télé 7 Jours",T7J,G),
  ("énième reportage à Gaza ( jamais au Soudan ou au Nigeria) où l'on prononce 12 fois le terme « génocide » . Le mensonge répété se transforme en mythe incrusté.","2026-10-10","X (@GWGoldnadel)","https://x.com/GWGoldnadel/status/2108986735938220224",G)])
P("jules-torres","Jules Torres","Journaliste au JDD, intervenant sur CNews",
 "Son affirmation sur l'évolution de la population de Gaza a été vérifiée et jugée fausse par 20 Minutes et France 24 ; Pascal Praud l'a contredit en direct. Il dit préférer le terme de « crimes de guerre ».",
 [("s'il s'agissait d'un génocide, ce serait le premier génocide de l'Histoire où la population augmente","2025-05-27","CNews, « L'Heure des Pros 2 », cité par 20 Minutes",MINUTES_TORRES,G)])
P("gerard-carreyrou","Gérard Carreyrou","Journaliste, intervenant sur Europe 1",
 "Intervenant de l'émission « Pascal Praud et vous » sur Europe 1.",
 [("Pour moi, le mot génocide ne correspond pas. C'est une guerre difficile, atroce (...) mais c'est la guerre","2025-10-01","Europe 1, « Pascal Praud et vous »",EU1_CARR,G)])
P("joseph-thouvenel","Joseph Thouvenel","Éditorialiste intervenant sur CNews",
 "Syndicaliste et éditorialiste invité sur CNews.",
 [("Un génocide, c'est faire disparaître volontairement un peuple, ce n'est absolument pas ce qu'il se passe à Gaza","2025-08-03","CNews",CNEWS_THOUV,G)])
P("elisabeth-levy","Élisabeth Lévy","Fondatrice et directrice de la rédaction de Causeur, éditorialiste sur Sud Radio",
 "Chroniqueuse sur Sud Radio et intervenante régulière de « L'Heure des pros » (CNews) depuis 2017.",
 [("Le Hamas voulait des milliers de morts palestiniens pour alimenter la haine d'Israël et des juifs.","2024-04-08","Sud Radio, « Le regard d'Élisabeth Lévy » (transcription automatique)","https://www.sudradio.fr/emission/le-regard-delisabeth-levy-566",G),
  ("on accuse Tsahal d'organiser une famine, ce qui est évidemment faux pour ce qui est de l'organisation. Il y a bien effectivement des éléments de famine, malheureusement.","2024-04-08","Sud Radio, « Le regard d'Élisabeth Lévy » (transcription automatique)","https://www.sudradio.fr/emission/le-regard-delisabeth-levy-566",G)])
P("yonathan-arfi","Yonathan Arfi","Président du CRIF",
 "S'exprimait lors du 38e dîner du CRIF en mai 2024.",
 [("L'accusation de génocide ne vise pas à protéger les Palestiniens, mais résonne comme un cri de ralliement pour stigmatiser les juifs","2024-05-06","BFMTV (discours au dîner du CRIF)",BFM_ARFI,G)])
P("jean-dominique-merchet","Jean-Dominique Merchet","Journaliste (L'Express, LCI, selon sa biographie X)",
 "Journaliste spécialiste des questions de défense.",
 [("Accuser Israël de génocide, c'est nazifier l'Etat juif. C'est, à mes yeux, la revanche d'Hitler.","2026-10-07","X (@jdomerchet)","https://x.com/jdomerchet/status/2107742270753558671",G)])
P("serge-klarsfeld","Serge Klarsfeld","Historien et avocat",
 "A déclaré en juin 2024 qu'il voterait RN en cas de duel RN–LFI, tout en votant pour le centre dans sa propre circonscription. Pas de déclaration retenue sur Gaza.",
 [("[en cas de duel RN-LFI, il voterait RN sans] hésitation","2024-06-15","LCI, cité par franceinfo",FI_KLARS,X),
  ("[le RN] a fait sa mue","2024-06-15","LCI, cité par franceinfo",FI_KLARS,X)])
P("vincent-bollore","Vincent Bolloré","Industriel, actionnaire de référence de Vivendi / Canal+",
 "Son groupe contrôle Canal+ (dont CNews) et, via l'OPA sur Lagardère, Europe 1, le JDD et Paris Match. Il s'est toujours défendu d'utiliser ces médias pour promouvoir ses opinions (franceinfo).",
 [])
P("geoffroy-lejeune","Geoffroy Lejeune","Directeur de la rédaction du JDD (depuis 2023), ancien directeur de Valeurs actuelles",
 "Sa nomination à la tête du JDD en 2023 a provoqué une longue grève de la rédaction.",
 [])

# ---------- ORGANISATIONS ----------
O("rn","Rassemblement national (ex-Front national)","Parti politique","Parti présidé par Jordan Bardella.")
O("reconquete","Reconquête","Parti politique","Parti fondé et présidé par Éric Zemmour.")
O("identite-libertes","Identité-Libertés","Mouvement politique","Mouvement lancé par Marion Maréchal en octobre 2024.")
O("lr","Les Républicains","Parti politique","Parti de droite, présidé par Éric Ciotti jusqu'en 2024.")
O("renaissance-epr","Renaissance / groupe EPR","Parti / groupe parlementaire","Parti et groupe parlementaire de la majorité présidentielle.")
O("vivendi-canal","Vivendi / Groupe Canal+","Groupe de médias","Groupe dont Vincent Bolloré préside le conseil de surveillance depuis 2014.")
O("lagardere","Lagardère","Groupe de médias","Groupe ayant fait l'objet d'une OPA de Vivendi (Europe 1, JDD, Paris Match).")
O("cnews","CNews","Chaîne d'information (Groupe Canal+)","Ex-i-Télé, renommée CNews.")
O("europe1","Europe 1","Radio (Lagardère / Vivendi)","Rapprochée de CNews en 2021.")
O("jdd","Le Journal du dimanche (JDD)","Hebdomadaire (Lagardère / Vivendi)","Dirigé par Geoffroy Lejeune depuis 2023.")
O("valeurs-actuelles","Valeurs actuelles","Hebdomadaire","Ancien employeur de Geoffroy Lejeune.")
O("franc-tireur","Franc-Tireur","Hebdomadaire (CMI France)","Lancé en 2021 ; Caroline Fourest directrice éditoriale, Raphaël Enthoven au comité de rédaction.")
O("causeur","Causeur","Magazine","Fondé et dirigé par Élisabeth Lévy.")
O("sud-radio","Sud Radio","Radio","")
O("le-point","Le Point","Hebdomadaire","")
O("crif","CRIF","Organisation représentative","Conseil représentatif des institutions juives de France.")
O("yad-vashem-fr","Comité français pour Yad Vashem","Association","")
O("conf-jerusalem-2025","Conférence sur l'antisémitisme, Jérusalem (mars 2025)","Événement","Conférence organisée à l'invitation du ministre israélien Amichai Chikli.")
O("avocats-sans-frontieres","Avocats sans frontières","Association","")
O("lexpress","L'Express","Hebdomadaire","")

# ---------- RELATIONS ----------
L("jordan-bardella","rn","président du parti",F24_BARDELLA,"2025-03-26")
L("marine-le-pen","rn","présidente du groupe des députés RN",HUFF_LEPEN,"2025-05-16")
L("eric-zemmour","reconquete","président du parti",EU1_ZEM,"2023-10-29")
L("eric-zemmour","cnews","ancien chroniqueur de « Face à l'info » (fin en septembre 2021)",FI_ZEM_CNEWS,"2021-09-13")
L("eric-zemmour","europe1","invité du Grand Rendez-Vous Europe 1 / CNews / Les Echos",EU1_ZEM,"2023-10-29")
L("marion-marechal","reconquete","ancienne vice-présidente, exclue après les législatives 2024",FI_MARECHAL_IL,"2024-10-07")
L("marion-marechal","identite-libertes","fondatrice",FI_MARECHAL_IL,"2024-10-07")
L("marion-marechal","marine-le-pen","a annoncé qu'elle la soutiendrait à la présidentielle 2027 (« candidate légitime du camp national »)",FI_MARECHAL_IL,"2024-10-07")
L("marion-marechal","rn","a négocié un accord législatif avec le RN (refusé par le RN le 11/06/2024)",FI_MARECHAL_JUIN,"2024-06-11")
L("marion-marechal","conf-jerusalem-2025","invitée",RMC_BARDELLA,"2025-03-19")
L("marion-marechal","cnews","invitée (déclaration du 21/05/2024)",CNEWS_MAR,"2024-05-21")
L("jordan-bardella","conf-jerusalem-2025","invité et participant",F24_BARDELLA,"2025-03-26")
L("bernard-henri-levy","conf-jerusalem-2025","a annulé sa participation en raison de l'invitation de Jordan Bardella",F24_BARDELLA,"2025-03-26")
L("eric-ciotti","lr","président du parti (en 2024)",BFM_CIOTTI,"2024-05-22")
L("eric-ciotti","rn","a annoncé une alliance électorale pour les législatives 2024",FI_CIOTTI,"2024-06-11")
L("identite-libertes","rn","propose une « coalition » avec Marine Le Pen, Jordan Bardella et Éric Ciotti",FI_MARECHAL_IL,"2024-10-07")
L("serge-klarsfeld","rn","a déclaré qu'il voterait RN en cas de duel RN–LFI",FI_KLARS,"2024-06-15")
L("marine-le-pen","serge-klarsfeld","a salué ses propos sur X",FI_KLARS,"2024-06-16")
L("eric-ciotti","serge-klarsfeld","a salué ses propos sur X",FI_KLARS,"2024-06-16")
L("meyer-habib","marine-le-pen","a qualifié son discours sur Israël d'« irréprochable »",HUFF_LEPEN,"2025-05-15")
L("meyer-habib","lr","ancien député apparenté LR",F24_YBP,"2023-10-22")
L("yael-braun-pivet","eric-ciotti","voyage commun en Israël (21-22 octobre 2023)",F24_YBP,"2023-10-22")
L("yael-braun-pivet","meyer-habib","voyage commun en Israël (21-22 octobre 2023)",F24_YBP,"2023-10-22")
L("yael-braun-pivet","renaissance-epr","membre",F24_YBP,"2023-10-22")
L("manuel-valls","europe1","invité (Europe 1 / CNews, 16/01/2025)",VP_VALLS,"2025-01-16")
L("caroline-yadan","renaissance-epr","députée du groupe EPR",FI_BERGE,"2025-07-22")
L("caroline-yadan","meyer-habib","lui a succédé comme députée de la 8e circonscription des Français de l'étranger",MARIANNE_YADAN,"2025-07-23")
L("caroline-yadan","le-point","autrice d'une tribune",
  "https://www.lepoint.fr/debats/qualifier-de-genocide-l-operation-menee-par-l-armee-israelienne-releve-de-la-manipulation-politique-09-09-2024-2569814_2.php","2024-09-09")
L("aurore-berge","caroline-yadan","soutient sa proposition de loi",FI_BERGE,"2025-07-22")
L("aurore-berge","renaissance-epr","membre du gouvernement (Renaissance)",FI_BERGE,"2025-07-22")
L("patrick-klugman","yad-vashem-fr","président",FI_BERGE,"2025-07-22")
L("robert-menard","rn","élu maire de Béziers en 2014 avec le soutien du Front national",F24_MENARD,"2014-03-28")
L("vincent-bollore","vivendi-canal","président du conseil de surveillance de Vivendi (depuis 2014)",FI_BOLLORE,"2023-06-25")
L("vivendi-canal","cnews","propriétaire (i-Télé renommée CNews)",FI_BOLLORE,"2023-06-25")
L("vivendi-canal","lagardere","OPA sur Lagardère",FI_BOLLORE,"2023-06-25")
L("lagardere","europe1","propriétaire",FI_BOLLORE,"2023-06-25")
L("lagardere","jdd","propriétaire",FI_BOLLORE,"2023-06-25")
L("europe1","cnews","rapprochement éditorial (2021)",FI_BOLLORE,"2023-06-25")
L("geoffroy-lejeune","jdd","directeur de la rédaction",FI_BOLLORE,"2023-06-25")
L("geoffroy-lejeune","valeurs-actuelles","ancien directeur",FI_BOLLORE,"2023-06-25")
L("gilles-william-goldnadel","cnews","chroniqueur","https://x.com/GWGoldnadel","2026-11-03")
L("gilles-william-goldnadel","avocats-sans-frontieres","président","https://x.com/GWGoldnadel","2026-11-03")
L("gilles-william-goldnadel","europe1","intervenant dans « Pascal Praud et vous »",T7J,"2025-10-01")
L("jules-torres","jdd","journaliste",MINUTES_TORRES,"2025-05-28")
L("jules-torres","cnews","intervenant dans « L'Heure des Pros 2 »",MINUTES_TORRES,"2025-05-27")
L("joseph-thouvenel","cnews","éditorialiste invité",CNEWS_THOUV,"2025-08-03")
L("gerard-carreyrou","europe1","journaliste intervenant",EU1_CARR,"2025-10-01")
L("elisabeth-levy","causeur","fondatrice et directrice de la rédaction",SUD_LEVY_BIO,"")
L("elisabeth-levy","sud-radio","éditorialiste et chroniqueuse",SUD_LEVY_BIO,"")
L("elisabeth-levy","cnews","intervenante dans « L'Heure des pros » (depuis 2017)",SUD_LEVY_BIO,"")
L("elisabeth-levy","robert-menard","co-autrice d'ouvrages",SUD_LEVY_BIO,"")
L("caroline-fourest","franc-tireur","directrice éditoriale et éditorialiste",STRAT_FT,"2022-04-07")
L("raphael-enthoven","franc-tireur","membre du comité de rédaction",STRAT_FT,"2022-04-07")
L("yonathan-arfi","crif","président",BFM_ARFI,"2024-05-06")
L("jean-dominique-merchet","lexpress","journaliste (biographie X)","https://x.com/jdomerchet","2026-11-03")
L("bernard-henri-levy","le-point","chroniqueur","https://bernard-henri-levy.com/fr/il-ny-a-pas-de-genocide-a-gaza-2/","2026-10-05")


# =====================================================================
# ---------- SECTION « France – normalisation de l'extrême droite » (v4) ----------
# =====================================================================
F="France – normalisation de l'extrême droite"; NU="Nuance / contexte"
GAZA_IDS={n["id"] for n in N}          # tous les nœuds antérieurs relèvent de la section Gaza
for _n in N:
    for _s in _n["statements"]: _s["section"]="gaza"   # déclarations antérieures : section Gaza
FI_DARM_ENS="https://www.franceinfo.fr/politique/jean-castex/gouvernement-de-jean-castex/securite-gerald-darmanin-dit-vouloir-stopper-l-ensauvagement-d-une-certaine-partie-de-la-societe_4055715.html"
BFM_DARM_ENS="https://www.bfmtv.com/politique/ensauvagement-darmanin-justifie-le-terme-et-se-refere-a-chevenement_AN-202007250131.html"
FI_DARM_LP="https://www.franceinfo.fr/politique/gerald-darmanin/laicite-immigration-violences-policieres-huit-sequences-a-retenir-de-l-emission-vous-avez-la-parole-avec-gerald-darmanin-et-marine-le-pen_4293225.html"
JDD_RET="https://www.lejdd.fr/politique/bruno-retailleau-au-jdd-il-faut-renverser-la-table-en-memoire-de-philippine-150010"
FIG_RET="https://www.lefigaro.fr/politique/l-etat-de-droit-n-est-pas-intangible-ni-sacre-apres-les-declarations-de-retailleau-braun-pivet-se-dit-assez-inquiete-20240930"
BFM_RET="https://www.bfmtv.com/politique/les-republicains/retailleau-deplore-une-regression-ethnique-des-emeutiers-les-insoumis-denoncent-son-racisme-crasse_AN-202307050457.html"
FI_RET_LR="https://www.franceinfo.fr/politique/bruno-retailleau/bruno-retailleau-est-elu-president-du-parti-les-republicains-avec-74-31-des-voix_7247163.html"
FI_PEC1="https://www.franceinfo.fr/elections/presidentielle/candidats/presidentielle-comment-valerie-pecresse-a-suscite-la-polemique-en-reprenant-la-theorie-d-extreme-droite-du-grand-remplacement_4960755.html"
FI_PEC2="https://www.franceinfo.fr/politique/valerie-pecresse/presidentielle-2022-valerie-pecresse-radicalise-son-discours_4961262.html"
FI_MACRON_VA="https://www.franceinfo.fr/politique/emmanuel-macron/dans-valeurs-actuelles-emmanuel-macron-veut-plus-d-efficacite-contre-l-immigration-illegale_3681211.html"
FI_PERICLES="https://www.franceinfo.fr/politique/front-national/plan-pericles-ce-que-l-on-sait-du-projet-du-milliardaire-catholique-pierre-edouard-sterin-pour-promouvoir-des-valeurs-conservatrices-et-faire-gagner-la-droite-aux-elections_6677268.html"
SO_CAMUS="https://www.sudouest.fr/justice/le-theoricien-du-grand-remplacement-renaud-camus-condamne-en-appel-pour-provocation-a-la-haine-raciale-9018188.php"
FI_ZEM_MINEURS="https://www.franceinfo.fr/politique/eric-zemmour/eric-zemmour-a-ete-definitivement-condamne-pour-complicite-de-provocation-a-la-haine-apres-ses-propos-tenus-sur-des-mineurs-isoles_7653920.html"
FI_CSA_CNEWS="https://www.franceinfo.fr/monde/europe/migrants/cnews-sanctionnee-d-une-amende-de-200-000-euros-pour-les-propos-d-eric-zemmour-sur-les-migrants-mineurs_4338041.html"
BFM_CIOTTI_ZEM="https://www.bfmtv.com/politique/presidentielle-ciotti-voterait-zemmour-contre-macron-au-deuxieme-tour_AD-202109050141.html"
FI_LEPEN_LOI="https://www.franceinfo.fr/societe/immigration/loi-immigration-le-rn-votera-pour-annonce-marine-le-pen-qui-revendique-une-victoire-ideologique_6254361.html"
FI_BARD_LOI="https://www.franceinfo.fr/societe/immigration/projet-de-loi-immigration-la-victoire-ideologique-du-rassemblement-national-est-de-plus-en-plus-forte-chaque-jour-se-targue-jordan-bardella_6253689.html"
FC_BARD_LIVRE="https://www.radiofrance.fr/franceculture/podcasts/l-economie-du-livre/les-livres-des-politiques-une-sortie-hors-normes-pour-le-premier-ouvrage-de-jordan-bardella-2577554"
FI_BOLLORE_CE="https://www.franceinfo.fr/economie/medias/devant-les-deputes-vincent-bollore-president-du-groupe-canal-assume-sa-foi-et-recuse-tout-projet-ideologique_6422296.html"
CE_CNEWS="https://www.conseil-etat.fr/actualites/pluralisme-et-independance-de-l-information-l-arcom-devra-se-prononcer-a-nouveau-sur-le-respect-par-cnews-de-ses-obligations"
FI_C8="https://www.franceinfo.fr/economie/medias/c8-et-nrj12-en-voie-de-perdre-leur-frequence-tnt-cinq-questions-sur-la-decision-de-l-arcom_6684051.html"
CC_LOI="https://www.conseil-constitutionnel.fr/actualites/communique/decision-n-2023-863-dc-du-25-janvier-2024-communique-de-presse"

def add_st(nid,*sts):
    n=[x for x in N if x["id"]==nid][0]
    n["statements"]+= [dict(zip(["quote","date","medium","url","theme"],s)) for s in sts]

# --- nouvelles personnes ---
P("gerald-darmanin","Gérald Darmanin","Ministre de la Justice ; ministre de l'Intérieur de 2020 à 2024",
 "A employé en juillet 2020 le terme « ensauvagement », utilisé auparavant par des responsables du RN selon franceinfo, et l'a justifié le lendemain. A débattu avec Marine Le Pen sur France 2 en février 2021.",
 [("Il faut stopper l'ensauvagement d'une certaine partie de la société.","2020-07-24","Le Figaro (entretien), cité par franceinfo",FI_DARM_ENS,F),
  ("[le terme résume] la réalité que subissent une partie des Français, notamment des milieux populaires","2020-07-25","Message sur X, cité par BFMTV",BFM_DARM_ENS,NU),
  ("Je trouve qu'en effet vous êtes plus molle que nous pouvons l'être","2021-02-11","France 2, « Vous avez la parole » (débat avec Marine Le Pen), cité par franceinfo",FI_DARM_LP,F)])
P("bruno-retailleau","Bruno Retailleau","Président des Républicains (depuis mai 2025), ancien ministre de l'Intérieur (2024-2025)",
 "Élu président de LR le 18 mai 2025. Ses propos de septembre 2024 sur l'État de droit ont suscité des réactions, dont celle de la présidente de l'Assemblée nationale, qui s'est dite « assez inquiète » (Le Figaro).",
 [("L'État de droit, ça n'est pas intangible ni sacré. C'est un ensemble de règles, une hiérarchie des normes, un contrôle juridictionnel, une séparation des pouvoirs. Mais la source de l'État de droit, c'est la démocratie, c'est le peuple souverain.","2024-09-29","Le Journal du dimanche (entretien)",JDD_RET,F),
  ("certes, ce sont des Français mais ce sont des Français par leur identité et malheureusement pour la deuxième, la troisième génération, il y a comme une sorte de régression vers les origines ethniques","2023-07-05","franceinfo, cité par BFMTV",BFM_RET,F)])
P("valerie-pecresse","Valérie Pécresse","Présidente de la région Île-de-France ; candidate LR à la présidentielle 2022",
 "A employé l'expression « grand remplacement » lors de son meeting du Zénith de Paris (13 février 2022), puis a précisé le lendemain sa position sur RTL.",
 [("Pas de fatalité. Ni au grand déclassement, ni au grand remplacement. Je vous appelle au sursaut.","2022-02-13","Meeting au Zénith de Paris, cité par franceinfo",FI_PEC1,F),
  ("ça veut dire 'Je ne me résigne pas, justement, aux théories d'Éric Zemmour et aux théories de l'extrême-droite'","2022-02-14","RTL, cité par franceinfo",FI_PEC2,NU)])
P("emmanuel-macron","Emmanuel Macron","Président de la République",
 "A accordé à l'hebdomadaire Valeurs actuelles un entretien publié le 31 octobre 2019, consacré notamment à l'immigration.",
 [("Je tiens au droit d'asile et je ne crois pas du tout qu'il faille avoir un discours simplificateur sur l'immigration","2019-10-30","Valeurs actuelles (entretien), cité par franceinfo",FI_MACRON_VA,NU)])
P("pierre-edouard-sterin","Pierre-Édouard Stérin","Entrepreneur et investisseur (Smartbox, Otium Capital), fondateur du Fonds du bien commun",
 "Le projet « Périclès », présenté dans un document de 2023 révélé par L'Humanité le 18 juillet 2024, est décrit comme fondé et administré par lui et deux proches ; ses équipes ont confirmé son existence (franceinfo).",
 [("[le document est] un peu daté","2024-07-20","Équipes de Pierre-Édouard Stérin, auprès du JDD, cité par franceinfo",FI_PERICLES,NU)])
P("renaud-camus","Renaud Camus","Écrivain, auteur du « Grand Remplacement » (2011)",
 "Théoricien du « grand remplacement ». Condamné en appel à Agen le 17 février 2022 à un mois d'emprisonnement avec sursis pour provocation publique à la haine raciale, pour des tweets (2017-2018) et un discours (Sud Ouest).",
 [("l'immigration est devenue invasion","2022-02-17","Propos poursuivis (tweets 2017-2018), cités par Sud Ouest (date de l'arrêt)",SO_CAMUS,F)])

# --- nouvelles organisations / institutions / événements ---
P("conseil-etat","Conseil d'État","Juridiction administrative suprême",
 "Saisi par Reporters sans frontières, a demandé le 13 février 2024 à l'Arcom de réexaminer le respect par CNews de ses obligations de pluralisme et d'indépendance.",
 [("l'Arcom doit prendre en compte la diversité des courants de pensée et d'opinions représentés par l'ensemble des participants aux programmes diffusés, y compris les chroniqueurs, animateurs et invités","2024-02-13","Décision du Conseil d'État (communiqué)",CE_CNEWS,F),
  ("[le Conseil d'État] ne se prononce pas sur le respect par les programmes de la chaîne CNews…","2024-02-13","Décision du Conseil d'État (communiqué)",CE_CNEWS,NU)],"org")
P("arcom","Arcom","Autorité de régulation de la communication audiovisuelle et numérique",
 "Régulateur de l'audiovisuel, issu en 2022 de la fusion du CSA et de la Hadopi. A décidé le 24 juillet 2024 de ne pas renouveler la fréquence TNT de C8.",
 [("en appréciant notamment l'intérêt de chaque projet pour le public au regard de l'impératif prioritaire de pluralisme des courants d'expression socio-culturels","2024-07-24","Décision de l'Arcom, citée par franceinfo",FI_C8,F)],"org")
O("conseil-constitutionnel","Conseil constitutionnel","Juridiction constitutionnelle",
 "Par sa décision n° 2023-863 DC du 25 janvier 2024, a censuré 32 articles de la loi immigration (sur 86) comme « cavaliers législatifs » et, au fond, partiellement ou totalement 3 autres articles.")
O("c8","C8","Chaîne de télévision (Groupe Canal+)",
 "Chaîne dont la fréquence TNT n'a pas été renouvelée par l'Arcom en juillet 2024 ; selon franceinfo, elle avait cumulé plus de 7,5 millions d'euros de sanctions.")
O("fayard","Fayard","Maison d'édition (Hachette Livre)",
 "Filiale de Hachette Livre, dont l'actionnaire est Vivendi (France Culture). A publié en novembre 2024 le livre de Jordan Bardella « Ce que je cherche ». Le 4 novembre 2026, elle organise au Pavillon Wagram (Paris) la soirée de lancement de son nouveau livre (BFMTV/AFP). StreetPress identifie cet ouvrage sous le titre « Gouverner » et présente Fayard comme détenue par Vincent Bolloré ; BFMTV/AFP qualifie le groupe Bolloré de « maison-mère » de Fayard.")
P("pericles","Projet « Périclès »","Projet de Pierre-Édouard Stérin (document de 2023)",
 "Plan présenté dans un document de 2023 révélé par L'Humanité le 18 juillet 2024 ; il prévoit environ 150 millions d'euros sur dix ans. Ses auteurs indiquent ne pas vouloir aider exclusivement le RN (franceinfo).",
 [("permettre la victoire idéologique, électorale et politique","2024-07-18","Document « Périclès » (2023) révélé par L'Humanité, cité par franceinfo",FI_PERICLES,F),
  ("300 villes à gagner absolument","2024-07-18","Document « Périclès » (2023), objectif fixé pour le RN aux municipales de 2026, cité par franceinfo",FI_PERICLES,F)],"org")
O("loi-immigration-2023","Loi immigration (2023)","Événement législatif",
 "Loi « pour contrôler l'immigration, améliorer l'intégration ». Texte adopté par le Parlement le 19 décembre 2023 après accord en commission mixte paritaire, avec le vote des députés RN ; partiellement censuré par le Conseil constitutionnel le 25 janvier 2024.")

# --- déclarations ajoutées à des personnes existantes (section France) ---
add_st("eric-zemmour",
 ("ils n'ont rien à faire ici, ils sont voleurs, ils sont assassins, ils sont violeurs, c'est tout ce qu'ils sont, il faut les renvoyer et il ne faut même pas qu'ils viennent","2020-09-29","CNews, « Face à l'info » (à propos des mineurs isolés) ; condamnation définitive par la Cour de cassation le 02/12/2025, selon franceinfo",FI_ZEM_MINEURS,F),
 ("C'est moi qui ai imposé ce terme dans la campagne présidentielle","2022-02-14","Cité par franceinfo (à propos du « grand remplacement »)",FI_PEC2,F))
add_st("eric-ciotti",
 ("Je voterais Eric Zemmour, très clairement","2021-09-05","Grand Jury RTL / LCI / Le Figaro, cité par BFMTV (hypothèse d'un second tour face à Emmanuel Macron)",BFM_CIOTTI_ZEM,F),
 ("nous n'avons pas la même histoire","2021-09-05","Grand Jury RTL / LCI / Le Figaro, cité par BFMTV (à propos d'Éric Zemmour)",BFM_CIOTTI_ZEM,NU))
add_st("marine-le-pen",
 ("On peut se réjouir d'une avancée idéologique (...), puisqu'il est inscrit maintenant dans cette loi la priorité nationale…","2023-12-19","Déclaration à l'Assemblée nationale, citée par franceinfo",FI_LEPEN_LOI,F),
 ("J'aurais pu le signer ce livre","2021-02-11","France 2, « Vous avez la parole » (à propos d'un livre de Gérald Darmanin), cité par franceinfo",FI_DARM_LP,F))
add_st("jordan-bardella",
 ("La victoire idéologique du Rassemblement national est de plus en plus forte chaque jour","2023-12-19","France Inter, cité par franceinfo",FI_BARD_LOI,F))
add_st("vincent-bollore",
 ("Je n'ai aucun projet idéologique, je suis tout doux et débonnaire, pas du tout un Attila","2024-03-13","Audition devant la commission d'enquête de l'Assemblée nationale sur la TNT, citée par franceinfo",FI_BOLLORE_CE,NU))

# --- relations (section France) ---
NE0=len(E)
L("gerald-darmanin","marine-le-pen","débat sur France 2, « Vous avez la parole » (11/02/2021)",FI_DARM_LP,"2021-02-11")
L("bruno-retailleau","lr","président du parti (élu le 18/05/2025)",FI_RET_LR,"2025-05-18")
L("bruno-retailleau","jdd","entretien publié le 29/09/2024",JDD_RET,"2024-09-29")
L("yael-braun-pivet","bruno-retailleau","s'est dite « assez inquiète » de ses propos sur l'État de droit",FIG_RET,"2024-09-30")
L("valerie-pecresse","lr","candidate LR à la présidentielle 2022",FI_PEC1,"2022-02-13")
L("emmanuel-macron","valeurs-actuelles","entretien accordé (paru le 31/10/2019)",FI_MACRON_VA,"2019-10-30")
L("eric-ciotti","eric-zemmour","a déclaré qu'il voterait pour lui dans l'hypothèse d'un second tour face à Emmanuel Macron",BFM_CIOTTI_ZEM,"2021-09-05")
L("eric-zemmour","renaud-camus","met en avant la théorie du « grand remplacement », popularisée par Renaud Camus (selon franceinfo)",FI_PEC1,"2022-02-14")
L("pierre-edouard-sterin","pericles","fondateur et administrateur du projet (selon le document révélé)",FI_PERICLES,"2024-07-20")
L("pericles","rn","le document vise une « victoire » du RN aux municipales de 2026",FI_PERICLES,"2024-07-20")
L("pericles","jdd","les équipes de P.-É. Stérin ont confirmé le projet auprès du JDD",FI_PERICLES,"2024-07-20")
L("jordan-bardella","fayard","auteur de « Ce que je cherche » (novembre 2024)",FC_BARD_LIVRE,"2024-11-09")
L("fayard","vivendi-canal","filiale de Hachette Livre, dont l'actionnaire est Vivendi",FC_BARD_LIVRE,"2024-11-09")
L("vivendi-canal","c8","propriétaire (Groupe Canal+)",FI_C8,"2024-07-24")
L("arcom","c8","non-renouvellement de la fréquence TNT (décision du 24/07/2024)",FI_C8,"2024-07-24")
L("arcom","cnews","amende de 200 000 € prononcée par le CSA (devenu Arcom) pour des propos d'Éric Zemmour",FI_CSA_CNEWS,"2021-03-18")
L("conseil-etat","arcom","demande de réexaminer le respect par CNews de ses obligations de pluralisme",CE_CNEWS,"2024-02-13")
L("conseil-etat","cnews","décision relative au pluralisme et à l'indépendance de l'information sur CNews",CE_CNEWS,"2024-02-13")
L("vincent-bollore","arcom","audition devant la commission d'enquête sur les fréquences TNT (Assemblée nationale)",FI_BOLLORE_CE,"2024-03-13")
L("marine-le-pen","loi-immigration-2023","a annoncé le vote des députés RN et parlé d'« avancée idéologique »",FI_LEPEN_LOI,"2023-12-19")
L("jordan-bardella","loi-immigration-2023","a évoqué une « victoire idéologique » du RN",FI_BARD_LOI,"2023-12-19")
L("rn","loi-immigration-2023","vote des députés RN en faveur du texte issu de la CMP",FI_LEPEN_LOI,"2023-12-19")
L("conseil-constitutionnel","loi-immigration-2023","censure partielle (décision n° 2023-863 DC du 25/01/2024)",CC_LOI,"2024-01-25")
for e in E[NE0:]: e["section"]="france"

# --- appartenance aux sections ---
FR_ALSO={"eric-zemmour","eric-ciotti","marine-le-pen","jordan-bardella","vincent-bollore","cnews","vivendi-canal","lagardere","jdd",
 "europe1","valeurs-actuelles","rn","lr","reconquete","geoffroy-lejeune","yael-braun-pivet"}
for n in N:
    sec=[]
    if n["id"] in GAZA_IDS: sec.append("gaza")
    if n["id"] not in GAZA_IDS or n["id"] in FR_ALSO: sec.append("france")
    n["sections"]=sec
for e in E: e.setdefault("section","gaza")

# --- photos et logos (Wikimedia Commons, licences libres) ---
import os
_here=os.path.dirname(os.path.abspath(__file__))
PIMG=json.load(open(os.path.join(_here,"tools/people_images.json")))
OLOG=json.load(open(os.path.join(_here,"tools/org_logos.json")))
for n in N:
    if n["id"] in PIMG: n.update(PIMG[n["id"]])
    if n["id"] in OLOG: n.update(OLOG[n["id"]])

# --- vidéos (diffuseur d'origine ou compte officiel ; vérifiées par curl / oEmbed) ---
def YT(vid,title,channel): return {"url":"https://www.youtube.com/watch?v="+vid,"platform":"youtube","id":vid,"title":title,"source":channel}
def PAGE(url,platform,title,source): return {"url":url,"platform":platform,"title":title,"source":source}
VIDEOS={
 ("eric-zemmour",0):YT("DBzVOTeT8M4","Eric Zemmour dans le Grand Rendez-Vous Europe 1 CNEWS spécial Israël/Hamas (29 octobre 2023)","Europe 1 (chaîne YouTube officielle)"),
 ("aurore-berge",0):YT("kmpRKPSrlI4","Dénoncer un génocide à Gaza, \"c'est une falsification historique\", estime Aurore Bergé","franceinfo (chaîne YouTube officielle)"),
 ("valerie-pecresse",0):YT("Jn_egqFvUmQ","Le discours de Valérie Pécresse au Zénith de Paris en intégralité","BFMTV (chaîne YouTube officielle)"),
 ("marine-le-pen",3):YT("eRw6gUoGSu8","Loi immigration : le RN votera pour, annonce Marine Le Pen qui revendique une \"victoire idéologique\"","FRANCE 24 (chaîne YouTube officielle)"),
 ("jordan-bardella",2):YT("jzW9e91ZTjo","Jordan Bardella : \"On ne peut pas faire de \"En même temps\" avec l'immigration\" (Grand Entretien, 19/12/2023)","France Inter (chaîne YouTube officielle)"),
 ("bruno-retailleau",1):YT("lpnv1K6MDZY","Violences urbaines : il y a un \"lien\" avec \"l'immigration\", assure Bruno Retailleau (entretien du 05/07/2023)","franceinfo (chaîne YouTube officielle)"),
 ("vincent-bollore",0):YT("_vDNinTdQHU","Vincent Bolloré : audition devant la commission d'enquête sur les fréquences TNT","LCP - Assemblée nationale (chaîne YouTube officielle)"),
 ("gilles-william-goldnadel",0):PAGE(CNEWS_GOLD,"cnews.fr","«Jamais Israël n'a voulu cibler un civil», soutient Gilles-William Goldnadel","CNews (site officiel)"),
 ("yonathan-arfi",0):PAGE(BFM_ARFI,"bfmtv.com","Yonathan Arfi (président du Crif) : « L'accusation de génocide ne vise pas à protéger les Palestiniens… »","BFMTV (site officiel)"),
 ("eric-ciotti",0):PAGE(BFM_CIOTTI,"bfmtv.com","« Elle s'est décrédibilisée » : Éric Ciotti souhaite que la France quitte la Cour pénale internationale","BFMTV (site officiel)"),
 ("jordan-bardella",1):PAGE(RMC_BARDELLA,"rmc.bfmtv.com","Jordan Bardella en Israël : « Je n'y vais pas pour parler du conflit », assure le président du RN","RMC (site officiel)"),
 ("marion-marechal",0):PAGE(CNEWS_MAR,"cnews.fr","Marion Maréchal : « Il n'y a pas de génocide à Gaza… »","CNews (site officiel)"),
 ("joseph-thouvenel",0):PAGE(CNEWS_THOUV,"cnews.fr","Guerre au Proche-Orient : « Un génocide, c'est faire disparaître volontairement un peuple… », analyse Joseph Thouvenel","CNews (site officiel)"),
 ("gerard-carreyrou",0):PAGE(EU1_CARR,"europe1.fr","Pascal Praud et vous – Conflit Israël-Hamas : « Le mot 'génocide' ne correspond pas » à la réalité, estime Gérard Carreyrou","Europe 1 (site officiel)"),
}
_by={n["id"]:n for n in N}
for (nid,i),v in VIDEOS.items(): _by[nid]["statements"][i]["video"]=v

# =====================================================================
# ---------- v5 : catégories / sous-catégories, sections des déclarations, archives ----------
# =====================================================================
for _n in N:
    for _s in _n["statements"]: _s.setdefault("section","france")
POL="Responsables politiques"; MED="Médias & propriétaires"; JOU="Journalistes & éditorialistes"
INT="Intellectuels & essayistes"; ORG="Organisations & institutions"; EVT="Événements"
CAT={
 # Responsables politiques
 **{i:(POL,"Gouvernement & exécutif") for i in ["aurore-berge","gerald-darmanin","emmanuel-macron","manuel-valls"]},
 **{i:(POL,"Parlementaires & élus") for i in ["caroline-yadan","meyer-habib","marine-le-pen","eric-ciotti","yael-braun-pivet","marion-marechal","robert-menard","valerie-pecresse"]},
 **{i:(POL,"Partis & dirigeants de parti") for i in ["jordan-bardella","eric-zemmour","bruno-retailleau","rn","reconquete","identite-libertes","lr","renaissance-epr"]},
 # Médias
 **{i:(MED,"Propriétaires, financeurs & groupes") for i in ["vincent-bollore","pierre-edouard-sterin","vivendi-canal","lagardere"]},
 **{i:(MED,"Chaînes, radios & titres") for i in ["cnews","c8","europe1","sud-radio","jdd","valeurs-actuelles","franc-tireur","causeur","le-point","lexpress"]},
 **{i:(MED,"Édition") for i in ["fayard"]},
 # Journalistes
 **{i:(JOU,"Directions de rédaction") for i in ["geoffroy-lejeune","elisabeth-levy","caroline-fourest"]},
 **{i:(JOU,"Journalistes & chroniqueurs") for i in ["jules-torres","gerard-carreyrou","joseph-thouvenel","jean-dominique-merchet","gilles-william-goldnadel"]},
 # Intellectuels
 **{i:(INT,"Philosophes & essayistes") for i in ["bernard-henri-levy","raphael-enthoven","renaud-camus"]},
 **{i:(INT,"Historiens") for i in ["serge-klarsfeld"]},
 # Organisations
 **{i:(ORG,"Institutions publiques") for i in ["conseil-etat","arcom","conseil-constitutionnel"]},
 **{i:(ORG,"Associations & représentants") for i in ["crif","yonathan-arfi","yad-vashem-fr","patrick-klugman","avocats-sans-frontieres"]},
 **{i:(ORG,"Projets & réseaux") for i in ["pericles"]},
 # Événements
 **{i:(EVT,"Événements") for i in ["conf-jerusalem-2025","loi-immigration-2023"]},
}
for _n in N:
    assert _n["id"] in CAT, "catégorie manquante : "+_n["id"]
    _n["category"], _n["subcategory"] = CAT[_n["id"]]
assert set(CAT) == {n["id"] for n in N}, set(CAT) - {n["id"] for n in N}
CATEGORY_ORDER=[POL,MED,JOU,INT,ORG,EVT]
# ---------- ajouts du 03/11/2026 ----------
# (a) ajouts de la routine quotidienne (commit c7dcb49), repris ici pour que la reconstruction ne les perde pas
HUFF_ARCOM_EZ="https://www.huffingtonpost.fr/france/article/l-arcom-a-directement-saisi-la-justice-pour-ces-sorties-d-eric-zemmour-apres-le-17-octobre_351273.html"
_by2={n["id"]:n for n in N}
_by2["eric-zemmour"]["statements"].append({"quote":"des hordes de barbares maghrébins et africains qui rentrent dans les villes","date":"2026-10-18",
 "medium":"LCI, au lendemain de la journée de mobilisation du 17 octobre 2026, cité par Le HuffPost avec AFP ; propos signalés au parquet par l'Arcom (annonce du 03/11/2026), aucune décision de justice à ce stade",
 "url":HUFF_ARCOM_EZ,"theme":F,"section":"france"})
_by2["arcom"]["statements"].append({"quote":"En tant qu'autorité publique, nous pouvons être conduits à signaler aux procureurs de la République des propos lorsqu'ils nous paraissent être attentatoires par exemple aux lois en matière d'appel à la discrimination. Cela a été fait par les services de l'Arcom la semaine dernière au sujet de propos tenus sur différentes antennes","date":"2026-11-03",
 "medium":"Martin Ajdari, président de l'Arcom, sur France Inter (L'invité du 13/14), cité par Le HuffPost avec AFP ; signalement au parquet visant des propos d'Éric Zemmour tenus sur LCI, BFMTV et CNews après la journée du 17 octobre 2026 ; à propos d'une telle saisine, M. Ajdari a déclaré : « ce n'est pas inédit mais c'est relativement rare »",
 "url":HUFF_ARCOM_EZ,"theme":F,"section":"france"})
L("arcom","eric-zemmour","signalement au parquet de propos tenus après la journée du 17 octobre 2026 sur LCI, BFMTV et CNews (annoncé le 03/11/2026)",HUFF_ARCOM_EZ,"2026-11-03")
E[-1]["section"]="france"
# (b) décisions de l'Arcom (approuvées le 03/11/2026) : texte des décisions publiées sur arcom.fr, articles de presse pour les liens
ARCOM_E1="https://www.arcom.fr/se-documenter/espace-juridique/decisions/decision-du-21-octobre-2026-mettant-en-demeure-la-societe-europe-1-telecompagnie"
ARCOM_CN_MED="https://www.arcom.fr/se-documenter/espace-juridique/decisions/decision-du-12-juin-2026-mettant-en-demeure-la-societe-dexploitation-dun-service-dinformation"
ARCOM_CN_SANC="https://www.arcom.fr/se-documenter/espace-juridique/decisions/decision-du-24-juillet-2026-portant-sanction-lencontre-de-la-societe-dexploitation-dun-service-dinformation-sesi"
PRESS_E1="https://www.lemonde.fr/economie/article/2026/10/26/europe-1-mise-en-demeure-par-l-arcom-apres-des-propos-de-nature-a-inciter-a-la-haine-tenus-a-l-antenne-par-sa-presentatrice-christine-kelly_6800838_3234.html"
PRESS_CN_MED="https://www.lefigaro.fr/medias/il-y-a-un-desequilibre-manifeste-et-repete-l-arcom-met-en-demeure-cnews-de-se-conformer-a-ses-obligations-de-pluralisme-des-opinions-20260615"
PRESS_CN_SANC="https://www.franceinfo.fr/economie/medias/l-arcom-inflige-une-sanction-de-200-000-euros-a-cnews-pour-deux-sequences-de-nature-a-inciter-a-la-haine-en-2025_8127374.html"
_by2["arcom"]["statements"]+=[
 {"quote":"Il en résulte un déséquilibre manifeste et durable qui caractérise un manquement de l'éditeur à l'obligation de respecter le pluralisme des courants de pensée et d'opinion dans les programmes d'information de la chaîne « CNews » sur le mois de mars 2025.",
  "date":"2026-06-12",
  "medium":"Décision de l'Arcom du 12 juin 2026 (publiée le 15 juin 2026) mettant en demeure la Société d'exploitation d'un service d'information (SESI), éditrice de CNews, de se conformer à l'avenir à l'exigence d'expression pluraliste des courants de pensée et d'opinion (articles 1er, 3-1 et 13 de la loi du 30 septembre 1986, délibération du 17 juillet 2024) ; décision rendue après une saisine de Reporters sans frontières (janvier 2026) et l'examen de 168 heures de programmes de mars 2025. Une mise en demeure n'est pas une sanction.",
  "url":ARCOM_CN_MED,"theme":F,"section":"france"},
 {"quote":"Une sanction pécuniaire d'un montant de 200 000 euros est prononcée à l'encontre de la Société d'exploitation d'un service d'information (SESI).",
  "date":"2026-07-24",
  "medium":"Décision de l'Arcom du 24 juillet 2026 (publiée le 29 juillet 2026), article 1er : manquements à l'article 15 de la loi du 30 septembre 1986 (incitation à la haine) et aux articles 2-3-2 et 2-2-1 des conventions de CNews (comportements discriminatoires, maîtrise de l'antenne), retenus pour deux séquences de « 100% Politique » des 2 juin et 1er septembre 2025 (propos d'Erik Tegnér et extrait d'une vidéo d'Éric Zemmour, selon franceinfo/AFP) ; pas de sanction pour « L'Heure des pros 2 » du 23 octobre 2025. CNews a annoncé un recours devant le Conseil d'État.",
  "url":ARCOM_CN_SANC,"theme":F,"section":"france"},
 {"quote":"Les propos selon lesquels « beaucoup » de « migrants sont des violeurs », qui assimilent la présence en France de ce groupe de personnes à un facteur majeur de risque pour la sécurité publique, sont de nature à inciter à la haine et à encourager des comportements discriminatoires à leur égard en raison de leur origine ou de leur nationalité.",
  "date":"2026-10-21",
  "medium":"Décision de l'Arcom du 21 octobre 2026 (publiée le 26 octobre 2026) mettant en demeure Europe 1 Télécompagnie, au sujet d'une séquence de l'émission du 26 janvier 2026 présentée par Christine Kelly (« Christine Kelly et vous », selon Le Monde et Le Parisien) (article 15 de la loi du 30 septembre 1986 ; articles 2-4 et 2-10 de la convention du 25 octobre 2023 : non-incitation à la haine, comportements discriminatoires, maîtrise de l'antenne). Une mise en demeure n'est pas une sanction ; Europe 1 a indiqué contester la décision et annoncé un recours gracieux auprès de l'Arcom.",
  "url":ARCOM_E1,"theme":F,"section":"france"},
]
L("arcom","cnews","mise en demeure de respecter le pluralisme des courants de pensée et d'opinion (décision du 12/06/2026, publiée le 15/06/2026)",PRESS_CN_MED,"2026-06-12"); E[-1]["section"]="france"
L("arcom","cnews","sanction pécuniaire de 200 000 € pour deux séquences de « 100% Politique » de 2025 (décision du 24/07/2026, publiée le 29/07/2026 ; recours annoncé par CNews)",PRESS_CN_SANC,"2026-07-24"); E[-1]["section"]="france"
L("arcom","europe1","mise en demeure pour une séquence de « Christine Kelly et vous » du 26/01/2026 (décision du 21/10/2026, publiée le 26/10/2026 ; contestée par Europe 1)",PRESS_E1,"2026-10-21"); E[-1]["section"]="france"

# ---------- ajout du 03/11/2026 (2) : fait judiciaire, Nantes ----------
# Personne privée : non nommée (ni prénom ni initiale). Aucune relation causale : pas de lien vers une chaîne ; seuls les propos du prévenu et de la procureure, attribués.
FV="France – montée des violences"
F3_LEGE="https://france3-regions.franceinfo.fr/pays-de-la-loire/loire-atlantique/nantes/menaces-racistes-armes-factices-telespectateur-de-cnews-un-habitant-de-lege-condamne-a-six-mois-de-prison-pour-vouloir-cramer-des-musulmans-3443592.html"
LP_LEGE="https://www.leparisien.fr/faits-divers/alcool-solitude-et-cnews-en-boucle-un-technicien-de-45-ans-condamne-apres-ses-menaces-de-mort-racistes-sur-facebook-03-11-2026-J4YLXBPWUVEEPFJLRLRLUVL22Q.php"
OF_LEGE="https://www.ouest-france.fr/societe/justice/ce-quon-voit-est-anxiogene-a-nantes-un-homme-condamne-apres-des-menaces-de-mort-a-caractere-raciste-sur-facebook-23d0dcec-d79a-11f1-9911-9179baff22e2"
N.append({"id":"proces-nantes-menaces-2026","name":"Condamnation pour menaces de mort racistes sur Facebook, Nantes (novembre 2026)","type":"org","role":"Événement judiciaire",
 "description":"Le lundi 2 novembre 2026 (audience tenue vers minuit selon Ouest-France ; France 3 date le jugement du 3 novembre), le tribunal correctionnel de Nantes, en comparution immédiate, a condamné un technicien de maintenance de 45 ans habitant Legé (Loire-Atlantique), interpellé après un signalement sur la plateforme PHAROS le 30 octobre 2026, à six mois d'emprisonnement avec sursis probatoire pour des menaces de mort à caractère raciste publiées sur Facebook visant des musulmans et Emmanuel Macron. Obligations : soins pendant deux ans, stage de citoyenneté ; interdiction de détenir une arme pendant cinq ans. Son avocate a présenté le compte Facebook comme « un exutoire ». Personne privée, non nommée ici. Sources : France 3 Pays de la Loire (3 novembre 2026) ; également rapporté par Le Parisien et Ouest-France (ce dernier indique un âge de 44 ans).",
 "statements":[
  {"quote":"Cramer toute cette merde de musulmans [...] comme Hitler l'a fait pour les Juifs.","date":"2026-11-02",
   "medium":"Propos publiés sur Facebook par le prévenu en octobre 2026, cités par France 3 Pays de la Loire ; jugement du tribunal correctionnel de Nantes (comparution immédiate) : six mois d'emprisonnement avec sursis probatoire pour menaces de mort à caractère raciste, visant aussi Emmanuel Macron",
   "url":F3_LEGE,"theme":FV,"section":"france"},
  {"quote":"Ça me monte un peu trop au cerveau, je suis une éponge","date":"2026-11-02",
   "medium":"Le prévenu, à l'audience du tribunal correctionnel de Nantes, au sujet de l'alcool qu'il consomme devant CNews pour « tromper sa solitude », cité par France 3 Pays de la Loire",
   "url":F3_LEGE,"theme":FV,"section":"france"},
  {"quote":"alimenté quotidiennement par des chaînes d'information en continu","date":"2026-11-02",
   "medium":"La procureure de la République, à l'audience, à propos du prévenu, citée par France 3 Pays de la Loire ; le tribunal a suivi les réquisitions du parquet",
   "url":F3_LEGE,"theme":FV,"section":"france"},
 ],
 "sections":["france"],"category":EVT,"subcategory":"Événements"})

# ---------- v10 (04/11/2026) : Cyril Hanouna, Némésis, ISSEP, M6 — éléments « Solide » uniquement ----------
AN_CR20="https://www.assemblee-nationale.fr/dyn/16/comptes-rendus/cetnt/l16cetnt2324020_compte-rendu.pdf"
LP_HAN_BOY="https://www.leparisien.fr/culture-loisirs/tv/guerre-israel-hamas-pour-cyril-hanouna-lappel-au-boycott-de-tpmp-est-un-acte-antisemite-31-10-2023-VQBIXKEHLNCJ7J4YSOI7QMIX5U.php"
M20_HAN_LFI="https://www.20minutes.fr/arts-stars/medias/4096418-20240615-elections-legislatives-2024-cyril-hanouna-europe-1-pendant-campagne-legislatives"
M20_HAN_W9="https://www.20minutes.fr/arts-stars/people/4203619-20260226-cyril-hanouna-indigne-propos-bruno-gaccio-quentin-deranque-juge-extremement-graves"
FIG_HAN_ARCOM="https://www.lefigaro.fr/politique/vous-me-voyez-a-la-tete-de-l-arcom-cyril-hanouna-dement-l-information-selon-laquelle-jordan-bardella-lui-aurait-propose-ce-poste-20260504"
HUFF_BARD_ARCOM="https://www.huffingtonpost.fr/politique/article/bardella-dement-avoir-propose-la-tete-de-l-arcom-a-hanouna-apres-les-revelations-de-mediapart_263379.html"
FI_HAN_M6="https://www.franceinfo.fr/culture/tv/cyril-hanouna/l-animateur-cyril-hanouna-annonce-rejoindre-le-groupe-m6-en-septembre_7100610.html"
FI_E1_MED="https://www.franceinfo.fr/elections/legislatives/legislatives-2024-l-arcom-met-en-demeure-europe-1-pour-manque-de-mesure-et-d-honnetete-dans-l-emission-de-cyril-hanouna_6629991.html"
ARCOM_E1_2024="https://www.arcom.fr/sites/default/files/2024-06/Arcom%20-%20MED%20Europe%201.pdf"
FI_C8_BOY="https://www.franceinfo.fr/economie/medias/insultes-de-cyril-hanouna-a-un-depute-la-chaine-c8-ecope-d-une-amende-record-de-3-5-millions-d-euros_5649680.html"
LD_NEM="https://www.ladepeche.fr/2026/02/16/mort-de-quentin-a-lyon-quel-est-ce-collectif-identitaire-nemesis-proche-de-lextreme-droite-13228324.php"
FI_ISSEP="https://www.franceinfo.fr/politique/front-national/video-marion-marechal-le-pen-les-petits-secrets-de-son-ecole-de-sciences-politiques_2766371.html"
def _st(q,d,m,u,t,sec="france"): return {"quote":q,"date":d,"medium":m,"url":u,"theme":t,"section":sec}
def _node(i,name,typ,role,desc,sts,cat,sub,secs=("france",)):
    N.append({"id":i,"name":name,"type":typ,"role":role,"description":desc,"statements":sts,"sections":list(secs),"category":cat,"subcategory":sub})
_node("cyril-hanouna","Cyril Hanouna","person","Animateur de télévision et de radio (TPMP sur C8 jusqu'en février 2025 ; Europe 1 ; W9 et Fun Radio depuis septembre 2025)",
 "Animateur de « Touche pas à mon poste » (TPMP) sur C8. Auditionné le 14 mars 2024 par la commission d'enquête de l'Assemblée nationale sur les fréquences TNT, dont le président a indiqué que l'Arcom était intervenue 21 fois à propos de ses émissions depuis 2017. Le 9 février 2023, l'Arcom a infligé à C8 une amende de 3,5 millions d'euros pour ses propos envers le député Louis Boyard (TPMP du 10 novembre 2022) (franceinfo). Le 27 juin 2024, l'Arcom a mis en demeure Europe 1 au sujet de son émission « On marche sur la tête » (décision n° 2024-582). Après l'arrêt de C8 sur la TNT le 28 février 2025, il a annoncé rejoindre le groupe M6 (W9 et Fun Radio) à partir du 1er septembre 2025 (franceinfo).",
 [_st("Quand la semaine dernière, il y a eu un boycott TPMP, vous croyez que c'est pas un acte antisémite ça ? Et bah moi je vous le dis, c'est un acte antisémite","2023-10-31","TPMP (C8), cité par Le Parisien",LP_HAN_BOY,G,"gaza"),
  _st("Il est vrai qu'à un moment, j'ai très souvent invité Éric Zemmour – même s'il n'est venu que deux fois. Si je l'ai fait, c'est parce qu'il faisait l'événement tous les jours !","2024-03-14","Audition devant la commission d'enquête sur les fréquences TNT, Assemblée nationale (compte rendu officiel n° 20)",AN_CR20,M),
  _st("Jean-Luc Mélenchon a été mon premier invité politique","2024-03-14","Audition devant la commission d'enquête sur les fréquences TNT, Assemblée nationale (compte rendu officiel n° 20)",AN_CR20,M),
  _st("j'ai passé autant de bons moments avec Jordan Bardella qu'avec Jean-Luc Mélenchon […] Ça ne veut pas dire que je disais aux spectateurs de voter pour Jean-Luc Mélenchon, ni que je leur conseille maintenant de voter pour Jordan Bardella","2024-03-14","Audition devant la commission d'enquête sur les fréquences TNT, Assemblée nationale (compte rendu officiel n° 20)",AN_CR20,M),
  _st("Je pense vraiment que C8 fait l'objet d'un acharnement.","2024-03-14","Audition devant la commission d'enquête sur les fréquences TNT, Assemblée nationale (compte rendu officiel n° 20)",AN_CR20,M),
  _st("Je regrette bien entendu mes propos sur Louis Boyard.","2024-03-14","Audition devant la commission d'enquête sur les fréquences TNT, Assemblée nationale (compte rendu officiel n° 20)",AN_CR20,NU),
  _st("LFI au pouvoir, je pars","2024-06-12","Europe 1, « On marche sur la tête », cité par 20 Minutes",M20_HAN_LFI,F),
  _st("Franchement, à un moment, est-ce qu'il n'y a pas des sanctions pour les hommes politiques à force de dire autant de bêtises ?","2026-02-26","W9, « Tout beau, tout n9uf », cité par 20 Minutes (à propos de propos d'un candidat LFI)",M20_HAN_W9,M),
  _st("C'est une vanne, c'est sûr !","2026-05-04","Réponse à Mediapart, citée par Le Figaro, au sujet d'une proposition de présidence de l'Arcom que Mediapart attribue à Jordan Bardella (été 2024) ; Jordan Bardella a déclaré sur X : « je n'ai jamais proposé “la tête de l'Arcom à Cyril Hanouna” » (Le HuffPost)",FIG_HAN_ARCOM,NU)],
 MED,"Animateurs & producteurs",("gaza","france"))
_node("nemesis","Collectif Némésis","org","Collectif identitaire",
 "Collectif fondé en 2019 par Alice Cordier (un pseudonyme). La Dépêche (16 février 2026) le décrit comme « proche du parti Reconquête et du Rassemblement national ».",[],ORG,"Projets & réseaux")
_node("issep","ISSEP","org","Établissement privé d'enseignement supérieur (Lyon)",
 "Institut fondé à Lyon en 2018 par Marion Maréchal. Selon franceinfo : frais d'inscription de 5 500 € par an, diplôme non reconnu par l'État.",[],ORG,"Projets & réseaux")
_node("m6","Groupe M6 (W9, Fun Radio)","org","Groupe audiovisuel",
 "Groupe audiovisuel privé, propriétaire notamment de W9 et Fun Radio. Cyril Hanouna y anime une émission quotidienne sur W9 et un programme sur Fun Radio depuis le 1er septembre 2025 (franceinfo).",[],MED,"Chaînes, radios & titres")
for _a in [("cyril-hanouna","c8","animateur de TPMP (jusqu'à l'arrêt de C8 sur la TNT, le 28/02/2025)",FI_HAN_M6,"2025-02-27"),
 ("cyril-hanouna","m6","animateur sur W9 et Fun Radio à partir du 01/09/2025 (annoncé le 27/02/2025)",FI_HAN_M6,"2025-02-27"),
 ("cyril-hanouna","europe1","animateur de « On marche sur la tête »",FI_E1_MED,"2024-06-27"),
 ("arcom","europe1","mise en demeure pour l'émission « On marche sur la tête » diffusée du 17 au 25/06/2024 (décision n° 2024-582 du 27/06/2024)",ARCOM_E1_2024,"2024-06-27"),
 ("arcom","c8","amende de 3,5 M€ pour les propos de Cyril Hanouna envers le député Louis Boyard (TPMP du 10/11/2022)",FI_C8_BOY,"2023-02-09"),
 ("marion-marechal","issep","fondatrice (Lyon, 2018)",FI_ISSEP,"2018"),
 ("nemesis","reconquete","décrit par La Dépêche comme « proche du parti Reconquête et du Rassemblement national » (16/02/2026)",LD_NEM,"2026-02-16"),
 ("nemesis","rn","décrit par La Dépêche comme « proche du parti Reconquête et du Rassemblement national » (16/02/2026)",LD_NEM,"2026-02-16")]:
    L(*_a); E[-1]["section"]="france"
for _i in ["nemesis","reconquete","rn","cyril-hanouna","c8","europe1","arcom","m6","marion-marechal","issep"]:
    _n=[x for x in N if x["id"]==_i][0]
    if "france" not in _n["sections"]: _n["sections"].append("france")
# ---------- mise à jour du 04/11/2026 : Pnat (RTL, 03/11/2026) ; Arcom → CNews (intervention publiée le 03/11/2026) ----------
# Personnes privées (suspects, victimes) non nommées. Aucun lien causal ajouté.
RTL_PNAT="https://www.rtl.fr/actu/justice-faits-divers/23-procedures-sur-rtl-le-procureur-national-antiterroriste-affirme-que-les-menaces-de-l-ultra-droite-radicale-violente-sont-en-croissance-7900692013"
ARCOM_CN_100PWE="https://www.arcom.fr/se-documenter/espace-juridique/decisions/emission-100-politique-week-end-diffusee-le-3-avril-2026-intervention-aupres-de-cnews"
_node("pnat","Parquet national antiterroriste (Pnat)","org","Parquet spécialisé (créé en 2019), dirigé par le procureur national antiterroriste Olivier Christen",
 "Le 3 novembre 2026 sur RTL, après l'attentat commis le 23 octobre 2026 à Trappes et La Verrière (Yvelines), qui a fait un mort et sept blessés et que le Pnat rattache à l'« ultradroite radicale violente », le procureur national antiterroriste Olivier Christen a indiqué que 23 procédures liées à l'ultradroite radicale violente ont été ouvertes depuis la création du Pnat (une à deux par an au départ, six en 2025, six « pour l'instant » en 2026), sur un total de 681 procédures dont 480 en matière djihadiste ; il a précisé que la menace principale reste, selon lui, djihadiste (RTL ; BFMTV). Le suspect, mis en examen et placé en détention provisoire, est présumé innocent ; il n'est pas nommé ici.",
 [_st("Le nombre de procédures liées à l'ultra-droite radicale violente est en croissance depuis quelques années","2026-11-03",
   "Olivier Christen, procureur national antiterroriste, invité de Marc-Olivier Fogiel sur RTL ; il a précisé : six procédures ouvertes en 2025, « six pour l'instant en 2026 », 23 au total, sur « 681 procédures dont 480 en djihadisme » (« quatre » en sept ans pour l'ultra-gauche radicale violente) ; selon lui, la menace principale reste djihadiste",
   RTL_PNAT,FV),
  _st("c'est pour faire clairement la part des choses entre ce qui sont des partisans d'une idéologie politique, de quelque segment qu'elle soit et des personnes qui se radicalisent dans une idéologie et, au-delà même de la radicalité, vont considérer que la seule façon de porter leur idéologie est de passer à la violence contre les personnes","2026-11-03",
   "Olivier Christen, procureur national antiterroriste, sur RTL, à propos de la terminologie « ultra-droite radicale violente » employée par son parquet",
   RTL_PNAT,FV)],
 ORG,"Institutions publiques")
_by2["arcom"]["statements"].append(_st("Compte tenu de la sensibilité des termes employés, une telle présentation était susceptible de créer une confusion sur la portée et l'auteur des propos tenus.","2026-10-14",
 "Arcom, intervention auprès de CNews (délibéré en collège le 14 octobre 2026, publiée le 3 novembre 2026) au sujet de l'émission « 100% Politique Week-end » du 3 avril 2026 consacrée à la situation judiciaire de Rima Hassan : l'Arcom relève que des propos du présentateur (« Donc, c'est vraiment un complot. C'est le complot juif ») sont intervenus après la lecture et la paraphrase d'un message de Jean-Luc Mélenchon sur X, sans marque claire de distanciation entre la citation, sa reformulation et le commentaire du journaliste ; elle a « appelé l'attention de la chaîne sur la nécessité de veiller, en toutes circonstances, au respect des exigences d'honnêteté et de rigueur ». Nuances de l'Arcom : la séquence s'inscrivait « dans le cadre d'une polémique politique, autorisant par nature une liberté de ton accrue » ; le caractère éventuellement diffamatoire relève du juge judiciaire et non de l'Arcom. Une intervention n'est ni une mise en demeure ni une sanction.",
 ARCOM_CN_100PWE,F))
L("arcom","cnews","intervention (rappel des exigences d'honnêteté et de rigueur de l'information) au sujet de « 100% Politique Week-end » du 03/04/2026 (délibéré le 14/10/2026, publiée le 03/11/2026 ; ni mise en demeure ni sanction)",ARCOM_CN_100PWE,"2026-10-14"); E[-1]["section"]="france"

ARCH_EXTRA={M20_HAN_LFI:("https://web.archive.org/web/20261104122526/"+M20_HAN_LFI,"2026-11-04"),
 FIG_HAN_ARCOM:("https://web.archive.org/web/20261104123431/"+FIG_HAN_ARCOM,"2026-11-04"),
 LD_NEM:("https://web.archive.org/web/20261104123458/"+LD_NEM,"2026-11-04")}

# ---------- v12 (05/11/2026) : groupes dissous d'extrême droite / ultradroite (décrets, Conseil d'État, presse) ----------
FI_GI_DISS="https://www.franceinfo.fr/politique/jean-castex/gouvernement-de-jean-castex/le-groupe-d-extreme-droite-generation-identitaire-dissous-en-conseil-des-ministres-annonce-gerald-darmanin_4318225.html"
FI_LP_GI="https://www.franceinfo.fr/politique/marine-le-pen/video-generation-identitaire-ce-qui-scandalise-m-darmanin-doit-fait-l-objet-d-une-dissolution-ca-ce-n-est-pas-l-etat-de-droit-denonce-marine-le-pen_4273347.html"
FI_RIEU="https://www.franceinfo.fr/elections/presidentielle/l-ancien-cadre-de-generation-identitaire-et-assistant-parlementaire-rn-damien-rieu-rejoint-eric-zemmour_4924131.html"
FI_ZOUAVES="https://www.franceinfo.fr/politique/eric-zemmour/le-gouvernement-dissout-le-groupuscule-d-ultradroite-les-zouaves-paris-notamment-soupconne-d-etre-implique-dans-les-violences-lors-du-meeting-de-zemmour-a-villepinte_4905269.html"
LEGI_ZOUAVES="https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044844463"
LEGI_CIVITAS="https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000048151580"
CE_CIVITAS="https://www.conseil-etat.fr/fr/arianeweb/CE/decision/2024-12-30/489498"
CE_REMPARTS="https://www.conseil-etat.fr/fr/arianeweb/CE/decision/2025-07-31/497252"
FI_GUD19="https://www.franceinfo.fr/politique/le-ministre-de-l-interieur-gerald-darmanin-va-proposer-la-dissolution-du-groupe-d-ultradroite-gud_6613242.html"
FI_GUD="https://www.franceinfo.fr/politique/gouvernement-de-gabriel-attal/le-gouvernement-a-dissous-le-syndicat-etudiant-gud-et-trois-autres-groupes-d-extreme-droite_6627165.html"
GRP="Groupes dissous (extrême droite / ultradroite)"
_node("generation-identitaire","Génération identitaire","org","Association d'extrême droite (2012-2021), dissoute",
 "Créée en 2012, siège historique à Lyon (franceinfo). Dissoute par décret en Conseil des ministres le 3 mars 2021 ; le décret, présenté par le ministre de l'Intérieur Gérald Darmanin, lui reproche un discours incitant à la discrimination, à la haine ou à la violence et la qualifie de possible « milice privée » (franceinfo). L'association a annoncé un recours devant le Conseil d'État (Le Monde, 03/03/2021).",
 [_st("Cette association et certains de ses militants doivent être regardés comme tenant un discours de haine incitant à la discrimination ou à la violence envers des individus en raison de leur origine, de leur race et de leur religion","2021-03-03","Décret de dissolution du 3 mars 2021, cité par franceinfo",FI_GI_DISS,F)],ORG,GRP)
_node("zouaves-paris","Les Zouaves Paris","org","Groupement de fait (apparu en 2017), dissous",
 "Groupement de fait dissous en Conseil des ministres le 5 janvier 2022 (décret du 5 janvier 2022). franceinfo indique que le décret lui reproche « de nombreux et récurrents agissements violents » et de « propager un discours ouvertement raciste », et que le groupe était soupçonné d'être impliqué dans les violences ayant visé des militants de SOS Racisme lors de la réunion électorale d'Éric Zemmour à Villepinte (5 décembre 2021).",
 [_st("nombreux et récurrents agissements violents","2022-01-05","Décret de dissolution du 5 janvier 2022 (Légifrance), cité par franceinfo",FI_ZOUAVES,F)],ORG,GRP)
_node("civitas","Civitas","org","Association (constituée en parti politique), dissoute",
 "Dissoute par décret du 4 octobre 2023. Le Conseil d'État a rejeté le 30 décembre 2024 le recours de l'association (décision n° 489498), retenant notamment des faits d'« exaltation de la collaboration » et des propos à connotation antisémite de responsables ; il relève qu'elle revêt le caractère d'un parti politique. Président : Alain Escada (selon la décision).",
 [_st("ces éléments, compte tenu de leur caractère précis et concordant, caractérisent l'existence de faits d'exaltation de la collaboration","2024-12-30","Conseil d'État, décision n° 489498 (rejet du recours contre le décret du 4 octobre 2023)",CE_CIVITAS,F)],ORG,GRP)
_node("les-remparts","Les Remparts (Lyon)","org","Groupement de fait (créé le 7 septembre 2021), dissous",
 "Groupement de fait lyonnais dissous par décret du 26 juin 2024, avec les associations La Traboule et Top Sport Rhône (franceinfo). Le Conseil d'État a rejeté le recours le 31 juillet 2025 (décision n° 497252) ; le décret se fonde notamment sur un discours « provoquant à la haine, la discrimination et la violence » selon la décision.",
 [_st("Le groupement de fait \" Les Remparts \", créé le 7 septembre 2021, se présente comme un \" nouveau complexe communautaire, culturel et sportif \".","2025-07-31","Conseil d'État, décision n° 497252",CE_REMPARTS,NU)],ORG,GRP)
_node("gud","GUD (Groupe union défense)","org","Organisation étudiante d'extrême droite, dissoute",
 "Dissous en Conseil des ministres le 26 juin 2024, en même temps que Les Remparts, La Traboule et Top Sport Rhône (franceinfo). Après l'annonce, le GUD Paris a dénoncé une « folle politique de répression » (franceinfo).",[],ORG,GRP)
add_st("gerald-darmanin",
 ("Ce sont des gens qui pensent qu'il y a une suprématie blanche, qui portent des propos antisémites extrêmement graves","2024-06-19","BFMTV, au sujet du GUD (annonce de la proposition de dissolution), cité par franceinfo",FI_GUD19,F))
add_st("jordan-bardella",
 ("Si demain je suis à la tête du pays, je n'aurai aucune forme de tolérance à l'égard de ceux qui se livrent à de la violence dans notre pays","2024-06-19","En réponse à l'annonce de Gérald Darmanin sur le GUD, cité par franceinfo (il a déclaré qu'il dissoudrait « toutes les organisations d'ultragauche et d'ultradroite », y compris le GUD)",FI_GUD19,NU))
add_st("marine-le-pen",
 ("Ce qui scandalise Gérald Darmanin doit faire l'objet d'une dissolution ? Ça ce n'est pas l'Etat de droit. J'appelle à faire attention à ça","2021-01-27","franceinfo (radio), au sujet de la dissolution envisagée de Génération identitaire",FI_LP_GI,F))
for _s in [x for x in N if x["id"] in ("gerald-darmanin","marine-le-pen","jordan-bardella")]:
    _s["statements"][-1]["section"]="france"
for _a in [("gerald-darmanin","generation-identitaire","a présenté le décret de dissolution (Conseil des ministres du 03/03/2021)",FI_GI_DISS,"2021-03-03"),
 ("marine-le-pen","generation-identitaire","s'est opposée sur franceinfo à la dissolution envisagée (27/01/2021)",FI_LP_GI,"2021-01-27"),
 ("eric-zemmour","generation-identitaire","a accueilli dans Reconquête Damien Rieu, présenté par franceinfo comme ancien cadre de Génération identitaire (« Bienvenue dans la Reconquête, cher Damien ! », 20/01/2022)",FI_RIEU,"2022-01-20"),
 ("gerald-darmanin","zouaves-paris","a annoncé la dissolution en Conseil des ministres (05/01/2022)",FI_ZOUAVES,"2022-01-05"),
 ("zouaves-paris","eric-zemmour","groupe soupçonné (franceinfo) d'implication dans les violences contre des militants de SOS Racisme lors de sa réunion électorale de Villepinte (05/12/2021)",FI_ZOUAVES,"2021-12-05"),
 ("conseil-etat","civitas","rejet du recours contre le décret de dissolution du 04/10/2023 (décision n° 489498)",CE_CIVITAS,"2024-12-30"),
 ("conseil-etat","les-remparts","rejet du recours contre le décret de dissolution du 26/06/2024 (décision n° 497252)",CE_REMPARTS,"2025-07-31"),
 ("gerald-darmanin","les-remparts","ministre de l'Intérieur lors de la dissolution du 26/06/2024 (franceinfo)",FI_GUD,"2024-06-26"),
 ("gerald-darmanin","gud","a proposé la dissolution, prononcée le 26/06/2024",FI_GUD,"2024-06-26"),
 ("gud","rn","qualifié par Gérald Darmanin de « groupe d'ultradroite très ami » avec « les dirigeants du Rassemblement national » (BFMTV, 19/06/2024, rapporté par franceinfo)",FI_GUD19,"2024-06-19"),
 ("jordan-bardella","gud","a déclaré qu'il dissoudrait le GUD, comme « toutes les organisations d'ultragauche et d'ultradroite », s'il arrivait à Matignon (19/06/2024)",FI_GUD19,"2024-06-19")]:
    L(*_a); E[-1]["section"]="france"
for _i in ["generation-identitaire","zouaves-paris","civitas","les-remparts","gud","gerald-darmanin","marine-le-pen","jordan-bardella","eric-zemmour","conseil-etat","rn"]:
    _n=[x for x in N if x["id"]==_i][0]
    if "france" not in _n["sections"]: _n["sections"].append("france")

ARCH_EXTRA['https://www.conseil-etat.fr/fr/arianeweb/CE/decision/2024-12-30/489498']=('https://web.archive.org/web/20261105063042/https://www.conseil-etat.fr/fr/arianeweb/CE/decision/2024-12-30/489498',"2026-11-05")
ARCH_EXTRA['https://www.conseil-etat.fr/fr/arianeweb/CE/decision/2025-07-31/497252']=('https://web.archive.org/web/20261105063100/https://www.conseil-etat.fr/fr/arianeweb/CE/decision/2025-07-31/497252',"2026-11-05")
# --- v14 : candidats à la présidentielle 2027 ---
PR27="Candidats à la présidentielle 2027"
FI_LFI7O="https://www.franceinfo.fr/monde/proche-orient/israel-palestine/attaque-du-hamas-contre-israel-la-position-de-lfi-cree-la-polemique-au-sein-de-la-nupes_6109152.html"
FI_REAC_PAL="https://www.franceinfo.fr/monde/palestine/mieux-vaut-tard-que-jamais-decision-courageuse-les-reactions-politiques-apres-l-annonce-d-emmanuel-macron-de-reconnaitre-l-etat-de-palestine_7396984.html"
FI_MAC_PAL="https://www.franceinfo.fr/monde/proche-orient/guerre/la-paix-est-possible-emmanuel-macron-annonce-que-la-france-va-reconnaitre-l-etat-de-palestine-en-septembre_7396969.html"
FIG_GLU="https://www.lefigaro.fr/politique/guerre-hamas-israel-raphael-glucksmann-refuse-le-terme-de-genocide-et-prefere-celui-de-carnage-20240312"
FI_ROU="https://www.franceinfo.fr/monde/proche-orient/israel-palestine/guerre-entre-israel-et-le-hamas-nous-allons-vers-le-genocide-il-est-en-cours-accuse-fabien-roussel_6416110.html"
FI_TROCA="https://www.franceinfo.fr/monde/palestine/gaza/guerre-a-gaza-le-ps-le-pcf-et-les-ecologistes-reunis-a-paris-pour-denoncer-le-genocide-commis-par-israel_7274295.html"
BFM_PHI="https://www.bfmtv.com/politique/est-ce-le-bon-moment-les-doutes-d-edouard-phillipe-quant-a-la-reconnaissance-de-l-etat-de-palestine_AN-202507250488.html"
BFM_ATT="https://www.bfmtv.com/politique/gouvernement/reconnaissance-d-un-etat-palestinien-gabriel-attal-assure-a-son-tour-que-ce-n-est-pas-un-tabou_AN-202405290686.html"
PS_ATT="https://www.publicsenat.fr/actualites/parlementaire/gaza-la-reconnaissance-dun-etat-palestinien-nest-pas-un-tabou-mais-doit-etre-utile-au-processus-declare-gabriel-attal"
FIG_BER="https://www.lefigaro.fr/elections/legislatives/et-la-on-va-tergiverser-xavier-bertrand-demande-l-exclusion-d-eric-ciotti-des-republicains-20240611"
FI_VIL="https://www.franceinfo.fr/monde/proche-orient/israel-palestine/dominique-de-villepin-denonce-un-crime-de-genocide-a-gaza-et-appelle-a-la-mobilisation-internationale_7411846.html"
M20_VIL="https://www.20minutes.fr/monde/israel/4166059-20250731-crime-lieu-gaza-crime-genocide-affirme-dominique-villepin"
_REAC="Message sur X, cité par franceinfo (réactions à l'annonce de la reconnaissance de l'État de Palestine)"
_node("jean-luc-melenchon","Jean-Luc Mélenchon","person","Fondateur de La France insoumise ; candidat déclaré à la présidentielle 2027 (entré en campagne le 03/05/2026, selon France 24)",
 "Candidat à l'élection présidentielle en 2012, 2017 et 2022. Le 7 octobre 2023, sa réaction et le communiqué du groupe parlementaire LFI-NUPES ont fait l'objet de critiques d'autres responsables politiques, dont la Première ministre Élisabeth Borne (franceinfo).",
 [_st("toute la violence déchaînée contre Israël et à Gaza ne prouv[ait] qu'une chose : la violence ne produit et ne reproduit qu'elle-même. Horrifiés, nos pensées et notre compassion vont à toutes les populations désemparées victimes de tout cela. Le cessez-le-feu doit s'imposer","2023-10-07","Message sur X, cité par franceinfo",FI_LFI7O,G,"gaza"),
  _st("La victoire morale est là mais on connaît la technique des annonces différées de Macron. Depuis des mois ce type de comportement encourage la durée du crime à Gaza. Pourquoi en septembre et pas maintenant ?","2025-07-24",_REAC,FI_REAC_PAL,G,"gaza")],POL,PR27,("gaza",))
_node("raphael-glucksmann","Raphaël Glucksmann","person","Député européen, coprésident de Place publique ; candidat à la présidentielle 2027 (vainqueur de la primaire PS / Place publique / GRS le 11/10/2026)",
 "Désigné candidat commun du Parti socialiste, de Place publique et de la Gauche républicaine et socialiste avec 66,13 % des voix (Touteleurope).",
 [_st("J'ai un emploi extrêmement précautionneux du terme génocide","2024-03-11","Quotidien (TMC), cité par Le Figaro",FIG_GLU,G,"gaza"),
  _st("Les Palestiniens ont le droit de vivre, et de le faire dans leur État. Pareille reconnaissance est un acte fort et juste","2025-07-24",_REAC,FI_REAC_PAL,G,"gaza")],POL,PR27,("gaza",))
_node("fabien-roussel","Fabien Roussel","person","Secrétaire national du Parti communiste français ; candidat déclaré à la présidentielle 2027 (06/09/2026)",
 "Le 10 mars 2024, ses propos sur Europe 1 comparant la situation à Gaza à des sièges historiques ont suscité une réaction du président du Crif, Yonathan Arfi (franceinfo).",
 [_st("On parlait d'un risque génocidaire. Ce que j'ai entendu, ce que je vois, c'est que nous allons vers le génocide. Il est en cours","2024-03-10","Europe 1, cité par franceinfo avec AFP",FI_ROU,G,"gaza"),
  _st("Non au nettoyage ethnique à Gaza et au génocide du peuple palestinien","2025-05-26","Rassemblement au Trocadéro (Paris), cité par franceinfo avec AFP",FI_TROCA,G,"gaza")],POL,PR27,("gaza",))
_node("marine-tondelier","Marine Tondelier","person","Secrétaire nationale des Écologistes ; candidate déclarée à la présidentielle 2027",
 "A participé le 26 mai 2025, avec les dirigeants du PS et du PCF, à un rassemblement au Trocadéro (Paris) sur la situation à Gaza (franceinfo).",
 [_st("Ce qui se joue à Gaza, c'est l'image que l'humanité se fait d'elle-même","2025-05-26","Rassemblement au Trocadéro (Paris), cité par franceinfo avec AFP",FI_TROCA,G,"gaza"),
  _st("Espérons que cette annonce aide les Gazaouis victimes d'un génocide en cours dès à présent, dans l'attente de sa concrétisation à la rentrée.","2025-07-24",_REAC,FI_REAC_PAL,G,"gaza")],POL,PR27,("gaza",))
_node("edouard-philippe","Édouard Philippe","person","Président d'Horizons, ancien Premier ministre (2017-2020) ; candidat déclaré à la présidentielle 2027",
 "S'est exprimé par communiqué le 25 juillet 2025 sur l'annonce par Emmanuel Macron de la reconnaissance de l'État de Palestine (BFMTV).",
 [_st("Il faudra reconnaître un État de Palestine et il ne faudra pas attendre qu'il n'y ait plus qu'un cimetière à reconnaître. Mais est-ce le bon moment? C'est pour le moins incertain","2025-07-25","Communiqué, cité par BFMTV",BFM_PHI,G,"gaza")],POL,PR27,("gaza",))
_node("gabriel-attal","Gabriel Attal","person","Secrétaire général de Renaissance, ancien Premier ministre (2024) ; candidat déclaré à la présidentielle 2027 (22/05/2026)",
 "Premier ministre lors des questions au gouvernement du 29 mai 2024 au Sénat, où il a été interrogé sur la situation à Gaza (BFMTV, Public Sénat).",
 [_st("La reconnaissance d'un État palestinien n'est pas un tabou","2024-05-29","Questions au gouvernement, Sénat, cité par BFMTV et Public Sénat",BFM_ATT,G,"gaza"),
  _st("Reconnaître unilatéralement, sans que ça ne produise aucun impact diplomatique ou sur le front de la guerre, ça ne serait pas participer à trouver une solution","2024-05-29","Questions au gouvernement, Sénat, cité par BFMTV",BFM_ATT,G,"gaza")],POL,PR27,("gaza",))
_node("xavier-bertrand","Xavier Bertrand","person","Président (LR) de la région Hauts-de-France ; candidat déclaré à la présidentielle 2027 (27/08/2026)",
 "Invité de TF1 le 11 juin 2024, il a demandé l'exclusion d'Éric Ciotti des Républicains après l'annonce par celui-ci d'un accord avec le Rassemblement national pour les législatives (Le Figaro).",
 [_st("En passant cet accord avec le Rassemblement national, il a fait le choix de la collaboration avec l'extrême droite","2024-06-11","TF1, cité par Le Figaro",FIG_BER,F),
  _st("Soit Éric Ciotti part tout de suite, soit il est exclu des Républicains.","2024-06-11","TF1, cité par Le Figaro",FIG_BER,F)],POL,PR27,("france",))
_node("dominique-de-villepin","Dominique de Villepin","person","Ancien Premier ministre (2005-2007) et ministre des Affaires étrangères ; candidat déclaré à la présidentielle 2027 (La France humaniste)",
 "A repris le 1er août 2025 sur X sa tribune publiée le 31 juillet 2025 dans Le Monde sur la situation à Gaza (franceinfo, 20 Minutes).",
 [_st("Un crime a lieu à Gaza, un crime de génocide","2025-07-31","Tribune publiée dans Le Monde, citée par 20 Minutes et franceinfo",M20_VIL,G,"gaza"),
  _st("Elle honore nos valeurs universelles, mais elle nous oblige immédiatement à agir","2025-07-24","Message sur X au sujet de la décision d'Emmanuel Macron, cité par franceinfo",FI_REAC_PAL,G,"gaza")],POL,PR27,("gaza",))
_mac=[x for x in N if x["id"]=="emmanuel-macron"][0]
_mac["statements"].append(_st("Fidèle à son engagement historique pour une paix juste et durable au Proche-Orient, j'ai décidé que la France reconnaîtra l'Etat de Palestine","2025-07-24","Message sur X, cité par franceinfo",FI_MAC_PAL,G,"gaza"))
_mac["statements"].append(_st("L'urgence est aujourd'hui que cesse la guerre à Gaza et que la population civile soit secourue","2025-07-24","Message sur X, cité par franceinfo",FI_MAC_PAL,G,"gaza"))
if "gaza" not in _mac["sections"]: _mac["sections"].append("gaza")
for _a,_sec in [(("xavier-bertrand","eric-ciotti","a demandé son exclusion des Républicains après l'accord avec le RN (TF1, 11/06/2024)",FIG_BER,"2024-06-11"),"france"),
 (("xavier-bertrand","lr","président LR de la région Hauts-de-France (Le Figaro)",FIG_BER,"2024-06-11"),"france"),
 (("yonathan-arfi","fabien-roussel","a réagi à sa comparaison de Gaza avec des sièges historiques (franceinfo, 10/03/2024)",FI_ROU,"2024-03-10"),"gaza"),
 (("gabriel-attal","emmanuel-macron","a repris au Sénat les mots du président sur la reconnaissance d'un État palestinien (BFMTV, 29/05/2024)",BFM_ATT,"2024-05-29"),"gaza"),
 (("edouard-philippe","emmanuel-macron","s'est interrogé sur le calendrier de la reconnaissance annoncée (communiqué, 25/07/2025)",BFM_PHI,"2025-07-25"),"gaza"),
 (("jean-luc-melenchon","emmanuel-macron","a réagi sur X à l'annonce de la reconnaissance de l'État de Palestine (24/07/2025)",FI_REAC_PAL,"2025-07-24"),"gaza"),
 (("raphael-glucksmann","emmanuel-macron","a réagi sur X à l'annonce de la reconnaissance de l'État de Palestine (24/07/2025)",FI_REAC_PAL,"2025-07-24"),"gaza"),
 (("marine-tondelier","emmanuel-macron","a réagi sur X à l'annonce de la reconnaissance de l'État de Palestine (24/07/2025)",FI_REAC_PAL,"2025-07-24"),"gaza"),
 (("dominique-de-villepin","emmanuel-macron","a réagi sur X à l'annonce de la reconnaissance de l'État de Palestine (24/07/2025)",FI_REAC_PAL,"2025-07-24"),"gaza"),
 (("fabien-roussel","marine-tondelier","rassemblement commun au Trocadéro sur la situation à Gaza (26/05/2025)",FI_TROCA,"2025-05-26"),"gaza")]:
    L(*_a); E[-1]["section"]=_sec
for _i in ["xavier-bertrand","eric-ciotti","lr"]:
    _n=[x for x in N if x["id"]==_i][0]
    if "france" not in _n["sections"]: _n["sections"].append("france")
for _i in ["yonathan-arfi","emmanuel-macron"]:
    _n=[x for x in N if x["id"]==_i][0]
    if "gaza" not in _n["sections"]: _n["sections"].append("gaza")

# v14 : archives Wayback (instantanés existants)
ARCH_EXTRA['https://www.franceinfo.fr/monde/proche-orient/israel-palestine/attaque-du-hamas-contre-israel-la-position-de-lfi-cree-la-polemique-au-sein-de-la-nupes_6109152.html']=('https://web.archive.org/web/20250822172642/https://www.franceinfo.fr/monde/proche-orient/israel-palestine/attaque-du-hamas-contre-israel-la-position-de-lfi-cree-la-polemique-au-sein-de-la-nupes_6109152.html',"2025-08-22")
ARCH_EXTRA['https://www.franceinfo.fr/monde/palestine/mieux-vaut-tard-que-jamais-decision-courageuse-les-reactions-politiques-apres-l-annonce-d-emmanuel-macron-de-reconnaitre-l-etat-de-palestine_7396984.html']=('https://web.archive.org/web/20261015215248/https://www.franceinfo.fr/monde/palestine/mieux-vaut-tard-que-jamais-decision-courageuse-les-reactions-politiques-apres-l-annonce-d-emmanuel-macron-de-reconnaitre-l-etat-de-palestine_7396984.html',"2026-10-15")
ARCH_EXTRA['https://www.franceinfo.fr/monde/proche-orient/guerre/la-paix-est-possible-emmanuel-macron-annonce-que-la-france-va-reconnaitre-l-etat-de-palestine-en-septembre_7396969.html']=('https://web.archive.org/web/20251219054155/https://www.franceinfo.fr/monde/proche-orient/guerre/la-paix-est-possible-emmanuel-macron-annonce-que-la-france-va-reconnaitre-l-etat-de-palestine-en-septembre_7396969.html',"2025-12-19")
ARCH_EXTRA['https://www.lefigaro.fr/politique/guerre-hamas-israel-raphael-glucksmann-refuse-le-terme-de-genocide-et-prefere-celui-de-carnage-20240312']=('https://web.archive.org/web/20240929102111/https://www.lefigaro.fr/politique/guerre-hamas-israel-raphael-glucksmann-refuse-le-terme-de-genocide-et-prefere-celui-de-carnage-20240312',"2024-09-29")
ARCH_EXTRA['https://www.franceinfo.fr/monde/palestine/gaza/guerre-a-gaza-le-ps-le-pcf-et-les-ecologistes-reunis-a-paris-pour-denoncer-le-genocide-commis-par-israel_7274295.html']=('https://web.archive.org/web/20250917175607/https://www.franceinfo.fr/monde/palestine/gaza/guerre-a-gaza-le-ps-le-pcf-et-les-ecologistes-reunis-a-paris-pour-denoncer-le-genocide-commis-par-israel_7274295.html',"2025-09-17")
ARCH_EXTRA['https://www.bfmtv.com/politique/est-ce-le-bon-moment-les-doutes-d-edouard-phillipe-quant-a-la-reconnaissance-de-l-etat-de-palestine_AN-202507250488.html']=('https://web.archive.org/web/20261105144054/https://www.bfmtv.com/politique/est-ce-le-bon-moment-les-doutes-d-edouard-phillipe-quant-a-la-reconnaissance-de-l-etat-de-palestine_AN-202507250488.html',"2026-11-05")
ARCH_EXTRA['https://www.bfmtv.com/politique/gouvernement/reconnaissance-d-un-etat-palestinien-gabriel-attal-assure-a-son-tour-que-ce-n-est-pas-un-tabou_AN-202405290686.html']=('https://web.archive.org/web/20250722000931/https://www.bfmtv.com/politique/gouvernement/reconnaissance-d-un-etat-palestinien-gabriel-attal-assure-a-son-tour-que-ce-n-est-pas-un-tabou_AN-202405290686.html',"2025-07-22")
ARCH_EXTRA['https://www.lefigaro.fr/elections/legislatives/et-la-on-va-tergiverser-xavier-bertrand-demande-l-exclusion-d-eric-ciotti-des-republicains-20240611']=('https://web.archive.org/web/20261105144144/https://www.lefigaro.fr/elections/legislatives/et-la-on-va-tergiverser-xavier-bertrand-demande-l-exclusion-d-eric-ciotti-des-republicains-20240611',"2026-11-05")
ARCH_EXTRA['https://www.20minutes.fr/monde/israel/4166059-20250731-crime-lieu-gaza-crime-genocide-affirme-dominique-villepin']=('https://web.archive.org/web/20260520132306/https://www.20minutes.fr/monde/israel/4166059-20250731-crime-lieu-gaza-crime-genocide-affirme-dominique-villepin',"2026-05-20")

# ---------- mise à jour du 05/11/2026 : « Gouverner », accès presse, pétition CNews ----------
BFM_GOUV="https://www.bfmtv.com/politique/front-national/mediapart-s-est-vu-refuser-l-acces-a-la-soiree-de-lancement-du-livre-de-jordan-bardella_AD-202611050240.html"
SP_GOUV="https://www.streetpress.com/1793883196-mediapart-politis-streetpress-rassemblement-national-bardella-tri-journalistes-antisemitisme-extreme-droite-fayard-bollore"
HUFF_CNEWS_PET="https://www.huffingtonpost.fr/politique/article/le-lr-alexandre-portier-rapporteur-sur-la-petition-anti-cnews-voici-les-prochaines-etapes-qui-attendent-le-texte_352080.html"
_b={n["id"]:n for n in N}
_b["jordan-bardella"]["statements"].append(_st(
 "l'extrême gauche (qui) manifeste contre... un livre […] nostalgie des régimes totalitaires chaque jour plus inquiétante",
 "2026-11-04",
 "Deux fragments d'un message sur X, cités par BFMTV/AFP (pas d'URL du message original consultée). BFMTV/AFP écrit qu'il accuse le premier et « développe selon lui » la seconde formule. Réaction, avant son arrivée, à un rassemblement d'une quinzaine de militants du collectif « Nous Vivrons » devant le Pavillon Wagram (Paris), le 4 novembre 2026, en marge de la soirée de lancement de son livre. Les slogans rapportés par BFMTV/AFP ne sont pas reproduits. Contexte indiqué par BFMTV/AFP : depuis la divulgation, fin septembre 2026, d'écrits de jeunesse antisémites attribués à Jordan Bardella, dans un climat de tension avec Mediapart, il nie catégoriquement et a déposé plainte pour diffamation. Ces écrits ne sont pas tenus pour établis ici.",
 BFM_GOUV, F))
_b["rn"]["statements"].append(_st(
 "C'est une soirée privée, ils ont été signifiés qu'ils n'étaient pas accrédités.",
 "2026-11-04",
 "Victor Chabert, directeur du service de presse du RN, cité par BFMTV/AFP. Le 4 novembre 2026, peu avant 20h, au Pavillon Wagram (Paris), un journaliste de Mediapart disposant d'un billet nominatif s'est vu refuser l'accès à la soirée de lancement du livre de Jordan Bardella organisée par Fayard. Le RN a invoqué le caractère « privé » de l'événement, auquel de nombreux autres médias étaient accrédités. La quasi-totalité des journalistes inscrits ont alors quitté les lieux, à l'exception notamment des médias du groupe Bolloré, présenté par BFMTV/AFP comme « maison-mère » de Fayard. StreetPress écrit en outre que ses journalistes se sont vu refuser l'entrée, et qu'une demande d'accréditation de Politis est restée sans réponse.",
 BFM_GOUV, F))
_b["rn"]["statements"].append(_st(
 "On fait ce qu'on veut.",
 "2026-11-04",
 "Victor Chabert, directeur du service de presse du RN, cité par StreetPress (qui le désigne aussi comme « responsable presse »), le 4 novembre 2026 au pavillon Wagram, devant des journalistes de Mediapart et de StreetPress, lors de la soirée de lancement de « Gouverner ».",
 SP_GOUV, F))
L("jordan-bardella","fayard","auteur de « Gouverner » (soirée de lancement le 04/11/2026 au pavillon Wagram). StreetPress présente Fayard, dont le service presse répond aux demandes d'accréditation, comme détenue par Vincent Bolloré, et écrit que des journalistes de Mediapart et de StreetPress se sont vu refuser l'entrée",SP_GOUV,"2026-11-04"); E[-1]["section"]="france"
L("vincent-bollore","fayard","BFMTV/AFP présente le groupe Bolloré comme « maison-mère » de Fayard ; à la soirée du 04/11/2026 au Pavillon Wagram, les médias de ce groupe sont restés après le départ de la quasi-totalité des autres journalistes inscrits",BFM_GOUV,"2026-11-04"); E[-1]["section"]="france"
L("rn","fayard","soirée de lancement du livre de Jordan Bardella organisée par Fayard le 04/11/2026 au Pavillon Wagram ; le RN invoque le caractère « privé » pour refuser l'accès à un journaliste de Mediapart muni d'un billet nominatif, alors que d'autres médias sont accrédités (BFMTV/AFP)",BFM_GOUV,"2026-11-04"); E[-1]["section"]="france"
L("vincent-bollore","cnews","le 04/11/2026, la commission des affaires culturelles et de l'éducation de l'Assemblée nationale désigne son président, le député LR Alexandre Portier, rapporteur de la pétition visant à « supprimer CNews » (plus de 800 000 signatures). Examen des suites envisagé possiblement le 10/11/2026 (LCP, cité par Le HuffPost). Le HuffPost présente CNews comme la « chaîne phare du groupe Bolloré ». Aucune décision de l'Assemblée à cette date",HUFF_CNEWS_PET,"2026-11-04"); E[-1]["section"]="france"

# ---------- mise à jour du 06/11/2026 : Le Pen et RN (CNews), Bardella/Bainville, Mélenchon (L'Avenir en commun) ----------
X_LP_CNEWS="https://x.com/MLP_officiel/status/2117897335271219295"
AN_QG_0411="https://questions.assemblee-nationale.fr/dyn/17/comptes-rendus/seance/session-ordinaire-de-2026-2027/premiere-seance-du-mercredi-04-novembre-2026"
FI_GOUV_LIVRE="https://www.franceinfo.fr/elections/presidentielle/gouverner-que-contient-le-nouveau-livre-de-jordan-bardella_8267120.html"
VOF_AEC="https://vof-news.fr/post/jean-luc-mlenchon-mise-tout-sur-gaza-au-dtriment-de-lukraine-dans-son-programme-pour-la"
EUR_AEC="https://fr.euronews.com/2026/11/06/lavenir-en-commun-jean-luc-melenchon-publie-son-programme-avant-un-grand-meeting"
I24_AEC="https://www.i24news.tv/fr/actu/france/artc-presidentielle-2027-melenchon-veut-voir-israel-devenir-un-etat-binational"
_b["marine-le-pen"]["statements"].append(_st(
 "Quoi qu’on puisse en penser, heureusement que CNEWS existe pour évoquer l’agression de jeunes catholiques à Rouen au cri de « sale blanc » et « sale facho », manifestation d’un racisme anti-Blancs dont quasiment aucun autre média n’a parlé. Refuser de parler et de condamner tous les racismes, c’est refuser de condamner le racisme.",
 "2026-11-04",
 "Message sur X (@MLP_officiel), 4 novembre 2026, 08:30 UTC. Le message publié comporte un saut de paragraphe avant la seconde phrase. Il porte sur la couverture, par CNews, d’une agression que Marine Le Pen situe à Rouen ; ce fait n’est pas documenté ici indépendamment de son message.",
 X_LP_CNEWS, F))
L("marine-le-pen","cnews","message public sur X (@MLP_officiel) le 04/11/2026 prenant la défense de CNews, qu’elle présente comme ayant évoqué une agression de jeunes catholiques à Rouen",X_LP_CNEWS,"2026-11-04"); E[-1]["section"]="france"
_b["rn"]["statements"].append(_st(
 "Une pétition réclame la fermeture de CNews. Voilà donc le projet démocratique de certains donneurs de leçons : museler ceux qui ne pensent pas comme eux.",
 "2026-11-04",
 "Frédéric Boccaletti, député RN, questions au gouvernement, Assemblée nationale, 4 novembre 2026 (compte rendu officiel, première séance). Le compte rendu insère, entre les deux phrases, la mention « (Applaudissements sur les bancs du groupe LFI-NFP.) ». Les interruptions d’autres députés figurent au compte rendu et ne sont pas reproduites.",
 AN_QG_0411, F))
_b["rn"]["statements"].append(_st(
 "Dans une démocratie, on combat des idées avec des arguments, pas avec des pétitions visant à censurer une chaîne de télévision.",
 "2026-11-04",
 "Frédéric Boccaletti, député RN, questions au gouvernement, Assemblée nationale, 4 novembre 2026 (compte rendu officiel). Phrase précédée, dans le même exposé, de : « Une ligne éditoriale se critique ; un journaliste se contredit ; une émission qui déplaît se zappe. »",
 AN_QG_0411, F))
_b["rn"]["statements"].append(_st(
 "L’Arcom a relevé qu’au premier trimestre 2026, plus de 70 % du temps de parole du Rassemblement national diffusé sur France Info et près de 60 % de celui diffusé sur France Inter l’avaient été entre minuit et 6 heures du matin.",
 "2026-11-04",
 "Frédéric Boccaletti, député RN, questions au gouvernement, Assemblée nationale, 4 novembre 2026 (compte rendu officiel). Phrase tenue par l’orateur au sujet de relevés qu’il attribue à l’Arcom ; le document de l’Arcom n’a pas été consulté pour cette entrée. La suite (« Voilà une conception bien particulière du pluralisme… ») n’est pas reproduite.",
 AN_QG_0411, F))
L("rn","cnews","Frédéric Boccaletti, député RN, a pris la défense de CNews aux questions au gouvernement du 04/11/2026 face à une pétition réclamant la fermeture de la chaîne (compte rendu officiel). Distinct de la désignation, le même jour, d’Alexandre Portier comme rapporteur de cette pétition",AN_QG_0411,"2026-11-04"); E[-1]["section"]="france"
_b["jordan-bardella"]["statements"].append(_st(
 "[la France n'est pas] une race [mais] une nation à laquelle on s'agrège",
 "2026-11-04",
 "Livre « Gouverner » (Fayard), sortie le 4 novembre 2026. franceinfo écrit que Jordan Bardella cite Jacques Bainville, qu'elle présente comme auteur nationaliste, royaliste et antisémite, « à qui il fait dire que la France n'est pas \"une race\" mais \"une nation à laquelle on s'agrège\" ». Les crochets reprennent cette liaison ; « une race » et « une nation à laquelle on s'agrège » sont les deux fragments placés entre guillemets par franceinfo.",
 FI_GOUV_LIVRE, F))
_b["jordan-bardella"]["statements"].append(_st(
 "L'aider à gagner cette campagne est ma responsabilité.",
 "2026-11-04",
 "Livre « Gouverner » (Fayard), cité par franceinfo, à propos de Marine Le Pen. franceinfo écrit qu'il reconnaît « avoir peut-être accusé le coup » après l'annonce de la candidature de Marine Le Pen, puis « se reprend » avec cette phrase.",
 FI_GOUV_LIVRE, F))
_b["jordan-bardella"]["statements"].append(_st(
 "On a tenté de me faire chuter",
 "2026-11-04",
 "Postface « Le prix de l'engagement » du livre « Gouverner » (Fayard), citée par franceinfo, qui écrit que Jordan Bardella « répète » cette phrase. franceinfo indique que les révélations de Mediapart sur des messages attribués à l'auteur à 17 ans sont arrivées alors que le livre était quasiment bouclé ; ces messages ne sont pas tenus pour établis ici. Il cite ensuite, selon franceinfo, une phrase attribuée à François Mitterrand : « Toutes les explications du monde ne justifieront pas qu'on ait pu livrer à la meute l'honneur d'un homme. »",
 FI_GOUV_LIVRE, F))
_b["jordan-bardella"]["statements"].append(_st(
 "Je sais maintenant que les mois qui viennent seront difficiles.",
 "2026-11-04",
 "Conclusion de la postface « Le prix de l'engagement » du livre « Gouverner » (Fayard), citée par franceinfo.",
 FI_GOUV_LIVRE, F))
_b["jean-luc-melenchon"]["statements"].append(_st(
 "autorités françaises […] laissé commettre […] génocide à Gaza",
 "2026-11-06",
 "Trois fragments du programme « L’Avenir en commun » (La Dispute, 160 pages, 4,90 euros), paru le 6 novembre 2026 selon Voice of Freedom. L’article écrit : « Reprochant aux « autorités françaises » d’avoir « laissé commettre » un « génocide à Gaza » ». La France insoumise avait annoncé le 2 novembre 2026 que cette parution serait la 5e édition (1 069 mesures). Le mot « un », entre le deuxième et le troisième fragment, n’est pas dans les guillemets de l’article.",
 VOF_AEC, G, "gaza"))
_b["jean-luc-melenchon"]["statements"].append(_st(
 "double standard diplomatique […] ne condamnant pas les guerres d’agression contre le Liban et l’Iran comme la guerre d’agression contre l’Ukraine",
 "2026-11-06",
 "Deux fragments du même programme, cités par Voice of Freedom le 6 novembre 2026. L’article écrit que le texte « accuse Emmanuel Macron d’avoir mené une politique de « double standard diplomatique » en « ne condamnant pas les guerres d’agression contre le Liban et l’Iran comme la guerre d’agression contre l’Ukraine » ».",
 VOF_AEC, G, "gaza"))
_b["jean-luc-melenchon"]["statements"].append(_st(
 "un génocide être commis […] deux poids, deux mesures",
 "2026-11-06",
 "Deux fragments rapportés par Euronews le 6 novembre 2026, dans une formulation distincte de celle de Voice of Freedom le même jour. Euronews écrit que le programme de LFI accuse le gouvernement français de laisser « un génocide être commis » à Gaza et dénonce ce qu’il décrit comme des « deux poids, deux mesures » diplomatiques.",
 EUR_AEC, G, "gaza"))
_b["jean-luc-melenchon"]["statements"].append(_st(
 "prendre en compte les autres possibilités […] État binational égalitaire",
 "2026-11-06",
 "Deux fragments du programme « L’Avenir en commun » (version dévoilée le 6 novembre 2026, 1 069 mesures selon i24NEWS). i24NEWS écrit que La France insoumise « propose désormais de « prendre en compte les autres possibilités » permettant de garantir les droits des Palestiniens, citant notamment l’hypothèse d’un « État binational égalitaire » ». i24NEWS écrit aussi, sans guillemets, que le texte promet des sanctions contre le gouvernement de Benyamin Netanyahou et la suspension de l’accord d’association entre Israël et l’Union européenne ; ces formulations ne sont pas reprises comme citations. Les qualifications éditoriales de l’article ne sont pas reprises.",
 I24_AEC, G, "gaza"))

# ---------- mise à jour du 07/11/2026 : Mélenchon (Bourget / X), Bardella (CNews, antifas) ----------
X_JLM_BOURGET="https://x.com/JLMelenchon/status/2119116481719882201"
X_JLM_DEDIE="https://x.com/JLMelenchon/status/2119099501218603276"
BFM_JLM_BOURGET="https://www.bfmtv.com/politique/elections/presidentielle/video-jean-luc-melenchon-veut-agir-frontalement-au-secours-des-palestiniens-contre-le-genocide-a-gaza-et-contre-l-annexion-progressive-de-la-cisjordanie-en-cas-de-victoire-a-l-election-presidentielle_VN-202611070422.html"
F24_BARD_CNEWS="https://www.france24.com/fr/info-en-continu/20261106-bardella-accuse-lfi-de-tentation-totalitaire-en-voulant-fermer-cnews"
X_CNEWS_BARD="https://x.com/CNEWS/status/2118796044427248034"
X_BARD_ANTIFA="https://x.com/J_Bardella/status/2118813222325153989"
_b["jean-luc-melenchon"]["statements"].append(_st(
 "Nous agirons frontalement au secours des Palestiniens, à la fois contre le génocide à Gaza et contre l’annexion progressive de la Cisjordanie.",
 "2026-11-07",
 "Message sur X (@JLMelenchon), 7 novembre 2026, 17:15 UTC. Présentation orale au meeting du Bourget le même jour ; BFMTV a aussi repris cette formulation ("+BFM_JLM_BOURGET+"). Engagement conditionnel à une éventuelle victoire présidentielle 2027 — le poste n’entraîne aucun ordre de déploiement.",
 X_JLM_BOURGET, G, "gaza"))
_b["jean-luc-melenchon"]["statements"].append(_st(
 "Les navires français, s’il le fallait, escorteront les flottilles de citoyens mobilisés pour faire valoir leurs droits.",
 "2026-11-07",
 "Même message sur X (@JLMelenchon), 7 novembre 2026, 17:15 UTC. Conditionnel (« s’il le fallait »). Distinct du programme écrit « L’Avenir en commun » déjà documenté le 06/11. Le même message se poursuit par deux phrases non reproduites ici.",
 X_JLM_BOURGET, G, "gaza"))
_b["jean-luc-melenchon"]["statements"].append(_st(
 "Je dédie chacune de nos rencontres au peuple palestinien, soumis au génocide à Gaza.",
 "2026-11-07",
 "Message sur X (@JLMelenchon), 7 novembre 2026, 16:07 UTC, en marge du meeting du Bourget. Le message dédie aussi le rassemblement aux victimes de l’attentat raciste de La Verrière et de Trappes ; cette seconde dédicace n’est pas reprise ici comme citation Gaza.",
 X_JLM_DEDIE, G, "gaza"))
_st_bard_cnews=_st(
 "Quand on veut fermer une chaîne de télévision comme CNews, on est habité d'une tentation totalitaire.",
 "2026-11-06",
 "Invité de Philippe de Villiers sur CNews (« HD Pros 2 WE » / #HDPros2WE), 6 novembre 2026, cité par AFP via France 24. La phrase suivante du même extrait AFP est reproduite séparément. Contexte indiqué par AFP : pétition demandant la fermeture de CNews (plus de 950 000 signatures le soir du 06/11) ; les députés doivent décider dans les prochains jours d’organiser ou non un débat ; le groupe parlementaire LFI est en première ligne. Aucune décision de l’Assemblée n’est documentée à cette date.",
 F24_BARD_CNEWS, F)
_st_bard_cnews["video"]={"url":X_CNEWS_BARD,"platform":"x.com","title":"Jordan Bardella sur CNews — « tentation totalitaire »","source":"CNews (compte officiel @CNEWS)"}
_b["jordan-bardella"]["statements"].append(_st_bard_cnews)
_b["jordan-bardella"]["statements"].append(_st(
 "Lorsque, comme le maire de Saint-Denis, on veut empêcher le Rassemblement national de pouvoir s'exprimer, on est pris d'une tentation totalitaire",
 "2026-11-06",
 "Même intervention sur CNews (« HD Pros 2 WE »), 6 novembre 2026, phrase suivant immédiatement la précédente dans la dépêche AFP reprise par France 24. La fonction est citée telle que dans la dépêche ; le nom de l’élu n’est pas repris.",
 F24_BARD_CNEWS, F))
L("jordan-bardella","cnews","invité dans « HD Pros 2 WE » le 06/11/2026 ; AFP via France 24 cite ses propos sur une « tentation totalitaire » à propos d’une demande de fermeture de CNews",F24_BARD_CNEWS,"2026-11-06"); E[-1]["section"]="france"
_b["jordan-bardella"]["statements"].append(_st(
 "Si je suis chef du gouvernement, je demanderai l'inscription des milices antifas et de toutes les organisations d'ultra-gauche sur la liste des organisations terroristes.",
 "2026-11-06",
 "Message sur X (@J_Bardella), 6 novembre 2026, 21:10 UTC. Phrase suivante du même post, non reproduite ici : « Il faudra faire cela pour protéger le droit à manifester des honnêtes gens. » AFP via France 24 rapporte la même intention, conditionnelle au fait qu’il devienne Premier ministre si Marine Le Pen est élue, dans une formulation proche (« demanderait à l’Union européenne l’inscription des milices antifas et de toutes les organisations d’ultragauche », sans trait d’union).",
 X_BARD_ANTIFA, F))

# ---------- mise à jour du 08/11/2026 : Caroline Yadan (X, citation de Mélenchon) ; contexte ambassadeur sur le Bourget ----------
X_YADAN_JLM="https://x.com/CarolineYADAN/status/2119194840160141660"
I24_ZARKA="https://www.i24news.tv/fr/actu/france/artc-melenchon-promet-d-agir-frontalement-contre-la-politique-israelienne-s-il-est-elu"
_b["caroline-yadan"]["statements"].append(_st(
 "Le vautour politique antisémite a encore sévi. Dans la lignée des dictateurs sanguinaires et des terroristes islamistes, il rêve, aux côtés des mollahs iraniens et du Hamas, de faire la guerre à Israël. Quand la haine devient une foi, la violence un devoir et la barbarie une vertu, il ne reste plus rien de la politique : seulement le fanatisme.",
 "2026-11-07",
 "Message sur X (@CarolineYADAN), 7 novembre 2026, 22:26 UTC. Le message publié comporte un saut de paragraphe avant « Quand la haine ». Les phrases reproduites sont celles de Caroline Yadan. Message publié en citation du message de Jean-Luc Mélenchon du 7 novembre 2026 ("+X_JLM_BOURGET+"), qui reprend son discours du Bourget sur Gaza, la Cisjordanie et les flottilles.",
 X_YADAN_JLM, G, "gaza"))
L("caroline-yadan","jean-luc-melenchon","a publié sur X, le 07/11/2026 à 22:26 UTC, un message en citation de celui de Jean-Luc Mélenchon du même jour sur Gaza, la Cisjordanie et les flottilles (discours du Bourget)",X_YADAN_JLM,"2026-11-07"); E[-1]["section"]="gaza"
_zarka_note=(" Contexte : le soir du 7 novembre 2026, Joshua Zarka, ambassadeur d’Israël en France, a réagi sur X. i24NEWS (article du 8 novembre 2026, "+I24_ZARKA+") écrit qu’il a partagé une vidéo du discours et cite, comme phrase du diplomate : « C'est une déclaration qui aurait fait honneur à l'un de ses prédécesseurs dans les mouvements fascistes européens des années trente du siècle dernier ». Les qualifications éditoriales de l’article ne sont pas reprises.")
for _s in _b["jean-luc-melenchon"]["statements"]:
    if _s["date"]=="2026-11-07" and _s["url"]==X_JLM_BOURGET and _s["quote"].startswith(("Nous agirons frontalement","Les navires français")):
        _s["medium"]+=_zarka_note

# ---------- v23 : parcours d'ascension + nature des liens ----------
# Une étape n'a un « by » que si la source nomme qui a désigné, nommé, confié ou chargé.
# Aucune causalité ajoutée. Pas de nouveau nœud.
_U_FI_PP="https://www.franceinfo.fr/politique/front-national/front-national-david-rachline-nomme-responsable-du-pole-communication-en-remplacement-de-florian-philippot_2382954.html"
_U_FI_4="https://www.franceinfo.fr/politique/front-national/europeennes-quatre-choses-a-savoir-sur-jordan-bardella-la-jeune-tete-de-liste-choisie-par-marine-le-pen_3142915.html"
_U_FI_19="https://www.franceinfo.fr/elections/europeennes/elections-europeennes-jordan-bardella-officiellement-choisi-comme-tete-de-liste-du-rassemblement-national_3133529.html"
_U_FI_VP="https://www.franceinfo.fr/politique/front-national/jordan-bardella-devient-vice-president-du-rassemblement-national_3492801.html"
_U_TF1_INT="https://www.tf1info.fr/politique/presidentielle-2022-pourquoi-marine-le-pen-laisse-sa-place-a-jordan-bardella-a-la-tete-du-rn-a-frejus-2196085.html"
_U_INTER="https://www.radiofrance.fr/franceinter/jordan-bardella-elu-a-la-tete-du-rassemblement-national-3154150"
_U_FI_24="https://www.franceinfo.fr/elections/europeennes/elections-europeennes-2024-jordan-bardella-confirme-qu-il-sera-tete-de-liste-du-rassemblement-national_6041243.html"
_U_FI_MAT="https://www.franceinfo.fr/politique/parlement-francais/assemblee-nationale/dissolution/legislatives-2024-pourquoi-marine-le-pen-veut-laisser-matignon-a-jordan-bardella-en-cas-de-large-victoire-du-rn_6599709.html"
_U_TF1_MAT="https://www.tf1info.fr/politique/elections/legislatives/dissolution-video-marine-le-pen-sur-tf1-jordan-bardella-sera-premier-ministre-en-cas-de-majorite-rn-aux-legislatives-2303374.html"
_U_FI_PHI="https://www.franceinfo.fr/elections/pourquoi-emmanuel-macron-a-choisi-edouard-philippe-pour-le-poste-de-premier-ministre_2192137.html"
_U_FI_ATT="https://www.franceinfo.fr/politique/remaniement/remaniement-gabriel-attal-est-nomme-premier-ministre-en-remplacement-d-elisabeth-borne_6292461.html"
_U_FI_ZEM="https://www.franceinfo.fr/elections/presidentielle/presidentielle-2022-premier-meeting-d-eric-zemmour-pour-lancer-sa-reconquete_4871171.html"
_U_FI_MLP="https://www.franceinfo.fr/politique/marine-le-pen-officiellement-proclamee-presidente-du-fn-recueille-67-65-des-voix-contre-32-35-pour-son-rival_231301.html"
_U_FI_JLM="https://www.franceinfo.fr/elections/presidentielle/de-la-securite-sociale-integrale-a-la-vie-republique-jean-luc-melenchon-presente-son-programme-pour-2017_1874861.html"
_U_FI_MAR="https://www.franceinfo.fr/elections/europeennes/europeennes-marion-marechal-designee-tete-de-liste-du-parti-reconquete-annonce-eric-zemmour_6047075.html"
_U_FI_RETI="https://www.franceinfo.fr/politique/gouvernement-de-michel-barnier/gouvernement-barnier-bruno-retailleau-figure-de-la-droite-conservatrice-a-l-interieur_6795379.html"
_U_F3_CIO="https://france3-regions.franceinfo.fr/provence-alpes-cote-d-azur/alpes-maritimes/nice/eric-ciotti-elu-president-du-parti-les-republicains-2672864.html"

def _step(date, title, text, url, source, by=None, verb=None):
    d={"date":date,"title":title,"text":text,"url":url,"source":source}
    if by and verb:
        d["by"]=by
        d["verb"]=verb
    return d

def _parcours(pid, steps):
    steps=sorted(steps, key=lambda s: s["date"])
    _b[pid]["parcours"]=steps
    for s in steps:
        if not s.get("by"):
            continue
        L(s["by"], pid, s["verb"], s["url"], s["date"])
        E[-1]["nature"]="ascension"
        E[-1]["section"]="france"

_parcours("jordan-bardella", [
 _step("2012","Adhésion au Front national",
  "Jordan Bardella rejoint le Front national.",
  _U_FI_VP,"franceinfo"),
 _step("2015","Conseiller régional d'Île-de-France",
  "Il est élu conseiller régional d'Île-de-France.",
  _U_FI_4,"franceinfo"),
 _step("2017-09-21","Porte-parole du Front national",
  "Marine Le Pen désigne trois porte-parole du Front national, dont Jordan Bardella, alors conseiller régional d'Île-de-France.",
  _U_FI_PP,"franceinfo", by="marine-le-pen", verb="a désigné porte-parole du Front national"),
 _step("2018-03","Direction de Génération nation",
  "Il devient président de Génération nation, branche jeunesse du Front national. L'article ne nomme pas la personne qui le désigne.",
  _U_FI_4,"franceinfo"),
 _step("2019-01-07","Tête de liste aux européennes de 2019",
  "Le bureau exécutif du Rassemblement national valide à l'unanimité le choix de sa présidente, Marine Le Pen, de le désigner tête de liste pour les élections européennes de mai 2019.",
  _U_FI_19,"franceinfo", by="marine-le-pen", verb="a désigné tête de liste aux européennes de 2019"),
 _step("2019-05-26","Scrutin européen du 26 mai 2019",
  "Il est tête de liste du Rassemblement national. La liste totalise un peu plus de 23\u00a0% des voix.",
  _U_FI_VP,"franceinfo"),
 _step("2019-06-16","Vice-président du Rassemblement national",
  "Il est nommé vice-président du Rassemblement national lors du conseil national à La Rochelle, et entre au bureau exécutif. L'article ne nomme pas l'auteur de la nomination.",
  _U_FI_VP,"franceinfo"),
 _step("2021-09-12","Présidence par intérim",
  "Marine Le Pen lui confie les rênes du Rassemblement national pour la campagne présidentielle de 2022. Elle déclare le faire conformément aux statuts et au vote des adhérents qui l'ont placé en tête d'une élection interne.",
  _U_TF1_INT,"TF1 Info", by="marine-le-pen", verb="a confié la présidence par intérim du RN"),
 _step("2022-11-05","Président du Rassemblement national",
  "Les adhérents l'élisent président du Rassemblement national avec 84,84 % des voix, face à Louis Aliot, lors du congrès du parti à Paris.",
  _U_INTER,"France Inter"),
 _step("2023-09-03","Tête de liste annoncée pour 2024",
  "Dans un entretien au Figaro cité par franceinfo, il confirme qu'il conduira la liste du Rassemblement national aux élections européennes de juin 2024, en tant que député européen sortant et chef de parti.",
  _U_FI_24,"franceinfo"),
 _step("2024-06-09","Élections européennes",
  "Au soir du 9 juin 2024, les élections européennes sont largement remportées par le Rassemblement national.",
  _U_FI_MAT,"franceinfo"),
 _step("2024-06-10","Annonce pour Matignon, sous condition",
  "Sur TF1, Marine Le Pen annonce que Jordan Bardella sera Premier ministre si le Rassemblement national obtient une majorité aux législatives anticipées. Elle parle d'un partage des rôles : elle vers la présidence de la République, lui vers Matignon. Cette phrase est conditionnelle : elle ne constate pas une nomination.",
  _U_TF1_MAT,"TF1 Info", by="marine-le-pen", verb="a annoncé qu'il serait Premier ministre en cas de majorité du RN"),
])
_parcours("marine-le-pen", [
 _step("2011-01-16","Présidente du Front national",
  "Elle est proclamée présidente du Front national au congrès de Tours, avec 67,65 % des voix, contre 32,35 % pour son rival.",
  _U_FI_MLP,"franceinfo"),
 _step("2021-09-12","Présidence par intérim confiée",
  "Elle confie les rênes du Rassemblement national à Jordan Bardella, alors vice-président, le temps de la campagne présidentielle de 2022.",
  _U_TF1_INT,"TF1 Info"),
 _step("2022-11-05","Fin de la présidence du parti",
  "Le congrès élit Jordan Bardella président du Rassemblement national. Marine Le Pen quitte cette fonction.",
  _U_INTER,"France Inter"),
])
_parcours("edouard-philippe", [
 _step("2017-05-15","Premier ministre",
  "Emmanuel Macron le nomme Premier ministre.",
  _U_FI_PHI,"franceinfo", by="emmanuel-macron", verb="a nommé Premier ministre"),
])
_parcours("gabriel-attal", [
 _step("2024-01-09","Premier ministre",
  "L'Élysée annonce sa nomination comme Premier ministre, en succession d'Élisabeth Borne. Le communiqué cité par franceinfo indique que le président de la République le charge de former un gouvernement. Le même article identifie ce président : Emmanuel Macron.",
  _U_FI_ATT,"franceinfo", by="emmanuel-macron", verb="a chargé de former le gouvernement, lors de la nomination au poste de Premier ministre annoncée par l'Élysée"),
])
_parcours("eric-zemmour", [
 _step("2021-09-13","Fin des chroniques sur CNews",
  "CNews met fin à ses chroniques de « Face à l'info », après la décision du CSA de décompter son temps de parole.",
  FI_ZEM_CNEWS,"franceinfo"),
 _step("2021-12-05","Lancement de Reconquête",
  "Lors de son premier meeting de candidat à l'élection présidentielle, à Villepinte, il lance le parti Reconquête.",
  _U_FI_ZEM,"franceinfo"),
])
_parcours("eric-ciotti", [
 _step("2022-12-11","Président des Républicains",
  "Les adhérents l'élisent président des Républicains avec 53,7 % des voix, face à Bruno Retailleau.",
  _U_F3_CIO,"franceinfo"),
 _step("2024-06-11","Alliance électorale annoncée",
  "Il annonce une alliance des Républicains avec le Rassemblement national pour les législatives anticipées.",
  FI_CIOTTI,"franceinfo"),
])
_parcours("bruno-retailleau", [
 _step("2024-09-21","Ministre de l'Intérieur",
  "franceinfo le présente comme nommé ministre de l'Intérieur par Michel Barnier. Il succède à Gérald Darmanin. Michel Barnier n'a pas de fiche dans ce jeu de données : l'étape ne crée pas de lien.",
  _U_FI_RETI,"franceinfo"),
 _step("2025-05-18","Président des Républicains",
  "Les adhérents l'élisent président des Républicains avec 74,31 % des voix, face à Laurent Wauquiez.",
  FI_RET_LR,"franceinfo"),
])
_parcours("marion-marechal", [
 _step("2022-05","Direction de l'ISSEP",
  "Elle quitte la direction de l'ISSEP, à Lyon. L'article indique qu'elle juge son engagement politique incompatible avec cette fonction.",
  _U_FI_MAR,"franceinfo"),
 _step("2023-09-06","Tête de liste de Reconquête",
  "Éric Zemmour déclare, dans un entretien au Figaro cité par franceinfo : « J'ai décidé de confier à Marion Maréchal la mission de conduire la liste de Reconquête pour les élections européennes. »",
  _U_FI_MAR,"franceinfo", by="eric-zemmour", verb="a confié la tête de liste de Reconquête aux européennes"),
])
_parcours("jean-luc-melenchon", [
 _step("2016-10-16","La France insoumise",
  "franceinfo indique qu'il présente « L'Avenir en commun » près de Lille, lors de la première convention du mouvement baptisé La France insoumise.",
  _U_FI_JLM,"franceinfo"),
])
_parcours("cyril-hanouna", [
 _step("2025-02-27","Arrivée annoncée au groupe M6",
  "Il annonce rejoindre le groupe M6. Il doit animer une émission quotidienne sur W9 et un programme sur Fun Radio à partir du 1er septembre. Le groupe M6 écrit se réjouir de cette arrivée. L'article ne nomme pas une personne qui l'aurait recruté.",
  FI_HAN_M6,"franceinfo"),
])
_parcours("vincent-bollore", [
 _step("2014","Présidence du conseil de surveillance de Vivendi",
  "Il accède à la présidence du conseil de surveillance de Vivendi, et par là de sa filiale Canal+. L'article ne nomme pas une personne qui l'aurait désigné.",
  FI_BOLLORE,"franceinfo"),
])
_parcours("geoffroy-lejeune", [
 _step("2023-06-25","Direction du JDD",
  "franceinfo relate l'annonce de son arrivée à la tête du Journal du dimanche, en provenance de Valeurs actuelles. L'article ne dit pas qui l'a nommé.",
  FI_BOLLORE,"franceinfo"),
])
_parcours("pierre-edouard-sterin", [
 _step("2024-07-18","Projet « Périclès »",
  "Un document de 2023 décrit le projet « Périclès ». Le 18 juillet 2024, L'Humanité en publie le contenu. Les équipes de Pierre-Édouard Stérin en confirment l'existence, selon franceinfo.",
  FI_PERICLES,"franceinfo"),
])

def _nature(e):
    if e.get("nature") in ("ascension","opposition","autre"):
        return e["nature"]
    rel=e["relation"].lower()
    # opposition ou contrôle : sanction, procédure, critique, rupture, dissolution
    if any(k in rel for k in (
        "amende","mise en demeure","non-renouvellement","sanction pécuniaire","censure",
        "signalement","audition","dissol","rejet du recours","réexaminer","pluralisme",
        "assez inquiète","exclusion","s'est opposée","a annulé","soupçonné","exclue",
        "refusé","supprimer cnews")):
        return "opposition"
    # ni nomination, ni soutien, ni financement : apparition, réaction, ouvrage, événement
    if any(k in rel for k in (
        "invité","intervenant","entretien","débat","tribune","auteur de","voyage commun","a réagi",
        "a repris","s'est interrogé","a salué","lui a succédé","en citation","rapprochement",
        "co-autrice","soirée","avancée idéologique","victoire idéologique","vote des députés",
        "rassemblement commun","a accueilli","qualifié par","proche du parti","le document vise",
        "ont confirmé","message public sur x","a publié sur x","a qualifié")):
        return "autre"
    # ascension : poste, investiture, soutien public, financement ou contrôle capitalistique documenté
    if any(k in rel for k in (
        "président","directrice","directeur","fondat","propriétaire","opa ","filiale",
        "maison-mère","député","animateur","journaliste","chroniqueur","éditorialiste",
        "membre","a souten","soutien","élu maire","candidate","alliance","voterait",
        "prend la défense","a pris la défense")):
        return "ascension"
    return "autre"

for e in E:
    e["nature"]=_nature(e)

# archives Wayback Machine (tools/archive.py -> tools/archives.json)
_root=_here if os.path.isdir(os.path.join(_here,"tools")) else "/workspace/gaza-site"
_ap=os.path.join(_root,"tools/archives.json")
ARCH=json.load(open(_ap)) if os.path.exists(_ap) else {}
for _u,(_a,_d) in ARCH_EXTRA.items(): ARCH.setdefault(_u,{"archive_url":_a,"archived":_d,"status":"saved"})
def _arch(o,key="url"):
    a=ARCH.get(o.get(key))
    if a and a.get("archive_url"): o["archive_url"]=a["archive_url"]; o["archived"]=a["archived"]
for _n in N:
    for _s in _n["statements"]:
        _arch(_s)
        if _s.get("video") and _s["video"].get("platform")!="youtube": _arch(_s["video"])
    for _s in _n.get("parcours") or []:
        _arch(_s)
for _e in E: _arch(_e)

ids={n["id"] for n in N}
for e in E: assert e["source"] in ids and e["target"] in ids, e
data={"meta":{"generated":datetime.date.today().isoformat(),
 "methodology":"Seules figurent des personnes pour lesquelles au moins une source primaire ou secondaire reconnue a été consultée (citation exacte, date, média, URL). Les citations sont reproduites telles que publiées ; les crochets [ ] signalent une reformulation de contexte par la source ou une coupure. Aucune qualification juridique n'est attribuée aux personnes : le champ « theme » est un simple classement thématique. Les éléments de nuance (rectifications, désaccords, démentis) sont inclus. Chaque URL a été testée le "+datetime.date.today().isoformat()+" (voir sources-check.md). Les dates des messages X sont en UTC. Ce jeu de données ne constitue pas une accusation : il documente des propos publics et des liens publics sourcés. Section « France – normalisation de l'extrême droite » (ajoutée en v4) : propos publics datés et décisions d'institutions (Conseil d'État, Arcom, Conseil constitutionnel) relatifs à la reprise de thèmes ou de termes associés à l'extrême droite et aux liens entre partis, médias et financeurs ; mêmes règles de sourçage, nuances et réponses incluses. Photos : fichiers Wikimedia Commons sous licence libre, avec auteur, licence et lien ; logos reproduits à seule fin d'identification. Vidéos : uniquement des publications du diffuseur d'origine ou d'un compte officiel, vérifiées à la date de mise à jour.",
 "counts":{}, "category_order":CATEGORY_ORDER, "sections":{"gaza":"Gaza","france":F}},"nodes":N,"edges":E}
data["meta"]["counts"]={"persons":sum(n["type"]=="person" for n in N),"orgs":sum(n["type"]=="org" for n in N),"edges":len(E),"statements":sum(len(n["statements"]) for n in N),
 "photos":sum(1 for n in N if n.get("image")),"logos":sum(1 for n in N if n.get("logo")),
 "videos":sum(1 for n in N for st in n["statements"] if st.get("video")),
 "france_nodes":sum("france" in n["sections"] for n in N)}
json.dump(data,open(os.path.join(_root,"data.json"),"w"),ensure_ascii=False,indent=2)
print(data["meta"]["counts"])
