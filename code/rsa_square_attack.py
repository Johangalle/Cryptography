#!/usr/bin/python3
#
# Written by Johan Galle
#
# Fermat based RSA attack
#
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/
#
# This module supports the miller_rabin function to check whether a given number is prime or not.
# This module also supports the random generation of primes
# as well as the random generation of safe primes.
# The function largest_prime_factor should be used with caution, i.e. use it with small numbers only.
#
# This is a pure Python implementation, not even using any of the Python standard built-in libraries.
#
# No part of this module should be used for cryptography in production.
# This module is strictly for education purposes.
#
import math

def isSquare(x):
    # Check http://burningmath.blogspot.be/2013/09/how-to-check-if-number-is-perfect-square.html 
    # for the criteria that led to this code.
    # The idea is that checking whether a number is a perfect square is an expensive operation
    # and should only be done when basic criteria indicate that the number could be a perfect square.
    # Note that the term "digital root" is identical to the remainder when dividing by 9
    if x == 1:
        return True
    if x%9 in [2,3,5,6,8]:
        return False
    finalDigit = x%10
    if finalDigit in [2,3,7,8]:
        return False
    final2Digits = x%100
    final2Digit = final2Digits//10
    if finalDigit == 6:
        if final2Digit in [0,2,4,6,8]:
            return False
    else:
        if final2Digit in [1,3,5,7,9]:
            return False
    if finalDigit == 5:
        if final2Digit != 2:
            return False
    if finalDigit == 0:
        if final2Digit != 0:
            return False    
    if finalDigit in [0,2,4,6,8]:
        if final2Digits%4 != 0:
            final3Digits = x%1000
            if final3Digits%8 != 4:
                return False
    if finalDigit in [1,3,5,7,9]:
        final3Digits = x%1000
        if final3Digits%8 != 1:
            return False    
    low = 0
    high = x // 2
    root = high
    while root * root != x:
        root = (low + high) // 2
        if low + 1 >= high:
            return False
        if root * root > x:
            high = root
        else:
            low = root
    return True

def highSquareRoot(x):
    # returns the integer higher than the square root
    # this function should only be used for x=p*q
    # so, when we are certain that x is not a perfect square
    if x == 1:
        return True
    low = 0
    high = x // 2
    root = high
    while root * root != x:
        root = (low + high) // 2
        if low + 1 >= high:
            return low+1
        if root * root > x:
            high = root
        else:
            low = root
    return low+1

def lowSquareRoot(x):
    # returns the integer lower than or equal to the square root
    if x == 1:
        return True
    low = 0
    high = x // 2
    root = high
    while root * root != x:
        root = (low + high) // 2
        if low + 1 >= high:
            return low
        if root * root > x:
            high = root
        else:
            low = root
    return low

def factor(n, verbose=False):
    x = highSquareRoot(n)
    max = 2*x
    i = 0
    bl = 0
    while x<max:
        i = i + 1
        nbl = i.bit_length()
        if nbl != bl:
            bl = nbl
            basis = pow(2,bl)
            step = basis//10
            if step < 1:
                step = 1
        if i%step == 0 and verbose:
            print ("trial ", i," x = ", x)
        sq = x**2 - n
        # sqr = int(math.sqrt(sq)+0.5)
        # sqr = lowSquareRoot(sq)
        # if sqr**2 = sq:
        if isSquare(sq):
            y = lowSquareRoot(sq)
            q = x + y
            p = x - y
            return p,q
        else:
            x = x + 1
    return 0,0

if __name__ == '__main__':
    import primes
    import time
    
    # distance = pow(2,522)
    # dimension = 1024
    
    distance = pow(2,1034)
    dimension = 2048
    #p = primes.findAPrime(pow(2,dimension - 1),pow(2,dimension))
    #q = primes.findAPrime(p+distance,p+2*distance)
    #n = p*q
    
    #distance = pow(2,1034)
    #p = primes.findAPrime(pow(2,2047),pow(2,2048))
    #q = primes.findAPrime(p+distance,p+2*distance)
    #n = p*q    
    
    t0= time.time()
    print ("start factorization")
    
    #n = 3366502043033
    #n = 26121310685428846102678235361188744796363857735420828439242201414390161488470284219367747398947597713959826702054663090748847095978595491922593943221833431538637171812854714415271267059742957922807862753600529366119834766694597853559861795396511116739081218201833708231052352269674552332028904508161691917141428351490846524625017611696950159621776683409917817186013540405309776851734117677109655660770881889551011914697654014678251356635549478714453353909070176889816513361890020340777156297813481952089442560875351010604944229634055037041188429907296204638317095296968612615685696318362724997716822909106631
    #n = 65817591079506596030959079652411737742255895814146293752350148985827090219483023712459018067733569890228407105772512775397640276832960261231935995764564210929051854801484903915870044772740676099537729256567331250545554986251296256148907260360540131296541333678723925912205075795242886682301816801229041
    #n = 65817591079506596030959079652411737742255895814146293752350148985827090219483023712459018067733569890228407105772512775397640276832960261231935997098260535383897543251476152364062135465215319677792985578286721885295563048986710732798227725228431883352804953445655585791285134169148786787397176735852283
    #n = 65817591079506596030959079652411737742255895814146293752350148985827090219483023712459018067733569890228407105772512775397640276832960261231937263566064859362218852708796486646244525940016485901513842768522610586090653816965098588668179898075801518018454291603829871176618985476311999373933122121523309
    #n = 65817591079506596030959079652411737742255895814146293752350148985827090219483023712459018067733569890228407105772512775406055339252579449594683000915472408596449386598771540438408253508922519536958938247974173415305127261628746632413825536639515566955582832907441681720302777029607620471494290054046879
    #n = 9073352560302807768704637774731144179226925199674247875558835553449209899993767560356865744948236984441605604253358664215810710801092291231871846993159932107728721401449580505689440488885144828098872871041651581468901866852235652916242904452469525142900517468822533226280660185950609185352504443664271
    #n = 27476138281022007983833712096051133854896228165456445811065335774656732633496335841264736913491553767516691350391831401282067046729321323557401442277368566694634724219778066502443975125606943303671616840736502896453468289871834718568170974597059649646443105708129592239651195820402775269319913272272148943266039399423275841293171735833553722464372864217474386592819257160319075954780141592991866960611452744676602300718641773636438327878838785912339438665475828584568336558666304786099053424362765925398458224455918915032989237400571577473431446610759142073018106418438829660573362869885468526494213305623271
    #n = 412023436986659543855531365332575948179811699844327982845455626433876445565248426198098870423161841879261420247188869492560931776375033421130982397485150944909106910269861031862704114880866970564902903653658867433731720813104105190864254793282601391257624033946373269391
    #n = 188198812920607963838697239461650439807163563379417382700763356422988859715234665485319060606504743045317388011303396716199692321205734031879550656996221305168759307650257059
    # this value requires 11 million trials
    # n = 12897579826146527926189258027994080694484225333040344105086491548427499807153754656291285366243394215728079744156131902792897420143137628925877993609185830174859195650095614301502222405971170939109936051596031039078746697463192666246134457288648231681151780905997701327387741061787346784758140016876866170049847932044631044506189020044720910768872174764435792810142202454756164132462968071901320658510552249961600635171144624602220351877133243580383743802551631638521886329854938945603224247998448596977500678755055979787706222436755716532494133891860294667941885752658157428247644611918513086004803810150291116967259
    # this value of n requires 2 million trials
    # n = 23989977081140878854189614031737383566001069613149554014963790743423119621945485043240974667873228033261044309563716483268103112952228630066244997708334627029612393651203551943522602330954569678341645805588326842511724076889059865537211137586121570166705847064538397076278109244599561281531811035034871285347229658938195756740941395370908737830163595408213846935414072137232401806984366309822036404798859852810624647724019796139001890769561950609727886134799063557113181056478770701318747543679891992379664607435674962759038771098666940004765512833461315499885026046074310472378403251820436742626270662256469304623203
    # this value of n requires 600,000 trials
    # n = 12771408562262880959599187166634953820897426473058200113942775864736152232260423185151284140902445086329853995595082717920082415540871817015022617892164961335005785261207524721925176018293671475825221423219365747975119587108204734123520754203224751414737733106103988452321246552716859951081732149661475002105480611906192614780395377911315668754962169801418459984923754506816308833420193222230291078519807169179134566780414691724104590082574313351159376602811043731126541159572067397046648893538592376418242126740406542448021186202182451175270805733435862679681698995947276190769925459091365356293218387051820027600647
    # n = 25224507456159163156575877796028456473662369736904878100933060887887244216120260281695328861739056294270643097794317308976759958367437549244808863772906680939521070489582647498438244915199705468395817575606597814019562913707562306397168764567686787293933393417031620511244511892437239390863502308155450078419924080263102978663897532365363981719762081750552627197211945486141442274528746322354522651902908903406950060094343722668988129318030729213169059762443357730983377434699924583492845212206319390320703622866477008711013644010886555820367734996512061432529391693421190426715896428082690439073605633199475981032823
    # n = 920023056597568985521887410624193351796192764425066163485396369316261941112583540940746007768257535784220141980992498976318761106811250550732939423219057809252744970440237915648762207033233887720630503157239556971659793496817087550224332641219870132315940770206543357766999440962974256454594643930291825566588301321734608022280316056530395237875223544524736933438131175689798938594617991045154455718029590033085213277238045837640501237304887069573513293833017490585713611342561028316958079099996299756546358624072906515145905487104932889284516049154640544269553973467000597819444399537166587985891360510936150326484102546268205859591088054798709027341365511010302180450313816969326173290636938759576466055157714417184256998433013398274237288241240895318331566965803935315965761259774624376985362649322095749762063654436763127460391056261663990428558246664772119139865492233113547225387252239995953790990453350985499302949806253899484892147567897608161771513479037994553503759640511585339818465781274869194424631724278443863930927233889482316162605124270278854049135676135398099607953185113426302612345180817066257517159309913311149761327164360406478751162089551120549994202326003141484386703333935129587769487283441652473564149468789
    n = 487544444003645070260976524232322671735128783484958620043257844547063649158343345206215605346117718439000244824567569341163359955295213473589772713936425490539066640746310049157796774746732412301616791522943635885548730061951117222742476593886583679185833934349424854241901390749979980488097653562726144832452092622721833768855322064958140290848203962298177983699050299281116956486030381842753190435086291247579187470590414432725118652123740430812903836218582556095739211315784264850739448719924562311159544400801428684107608537167888888954387433984012149255109562281783481838272784056049857744060483682351059275834834847581497905323029206001976470084678320894665635115506387899931433926909237129807209583802635697924110762187986487274116046898502243225666829131458630424652181704404321085688066997378344243661117052279135009380533486407392479763640183275884727621771533613358161739761069212035947801551673515775368059051895837456127469124789053485223453748761150777496800318008824875859217523141574737782324035476388859892997885960942697978100918279301421606574882386037324301423182704323032420507591295898342551830453768898985005392316285635230475638957634452414179786326709003278611357753147260879052579735742017186486722985896457
    n = 341708860755414627517636563737860247694830833438797657665956672468749172737337997411628630654035938329379904059410124228607009461263361069116847161259105255138742079294267425342794529657129825331147410352448839693997261010063688808162779291721751425712075294479847191106434826340717256947538049838702515998263365869509608430695183643598865999140112212093073123305167653200522553656183728041470420591199945135496499334164435200008969152265966971403602979493823981768582344951065369666299023098642064754467705751906245031523259465290121218499615157083656389498127930396343025522145537248554593082156474616584338969385073825448979763530748132622565106892806741755646597542329567645916387865855622535243200382632354552022853571463780461007397238110014336165192703853377630034104881015278305508442723432179124941184007302116899991981921973313107714903711162613546496438380371854181593622445588617748330870154155167775411326048335944409023467407426270050642668622426447430610313523839555363085755645115241983447453246928258811007061312671762631440052193694702105558755799451629711020767678953504189487091100565445376360620206366417534234967330401645896676678940569449968918350637534292284674033833449148393767208207546335392476058733526333
    n = 341708860755414627517636563737860247694830833438797657665956672468749172737337997411628630654035938329379904059410124228607009461263361069116847161259105255138742079294267425342794529657129825331147410352448839693997261010063688808162779291721751425712075294479847191106434826340717256947538049838702515998473177809393765445959119317387244345439227071183143501319959333729226841697946311547263745007141688027857397797093412801410015933252420161615644700079606048711114825079121250322924191720923817017865778981879429155913922391731764709492656927370005111366992000634641587396557857422671415907133365861223160749601411599777362653334047509887391893703785858075592767173150807212362100144145460412169544319597424945553719393081684021060397796277295572211805047492475926500818866722386322994857045171241271239312184432717111691471822226211734426321206197761364961297521959398087760034633434420731447302570719084950309779375552351481010459777325573307436315094264376618638582978254557100365396735567006396394469928475016231258524552921462615137659203079579741476093321014818428449064793519514164363883337582004330438807891821403657958108237974905480927931273739083303517970217336187844752434754446452237718809936625698056376227548619851
    # n = 341708860755414627517636563737860247694830833438797657665956672468749172737337997411628630654035938329379904059410124228607009461263361069116847161259105255138742079294267425342794529657129825331147410352448839693997261010063688808162779291721751425712075294479847191106434826340717256947538049838702515999605477737814539507461482958208217832001654906428609294670981431708239519975760224167162965883255563080969678819336827357116843767951564821648569178045820428204175762591082444818717364464407951941971606085740333525541803072657460043870118239335947653386353688978688411014446672387410342844504796179832442432516213683576280499042811910325451740078145694525197109311536401111940878021867530800380565979400244930861554608914348506800371272857622124590125877980272975724427805488993427411275730894648138862610811263980653634088749310033841100446125785856461881946689955412063283023124298925564197529712346224365770576932090813671443508185710976892996751059136789460228635799934096464171094867530879063596401568403638549883175241338110538717296368076608313029289635756426606069626131828943894540521046239649485191608386944105862663909092648164662490207600700537314923255529797005890590774810028641986484132364180003123501633206754649
    n = 341708860755414627517636563737860247694830833438797657665956672468749172737337997411628630654035938329379904059410124228607009461263361069116847161259105255138742079294267425342794529657129825331147410352448839693997261010063688808162779291721751425712075294479847191106434826340717256947538049838702515998473177809393765445959119317387244345439227071183143501319959333729226841697946311547263745007141688027857397797093412801410015933252420161615644700079606048711114825079121250322924191720923817017865778981879429155913922391731764709492656927370005111366992000634641587396557857422671415907133365861223160749601411599777362653334047509887391893703785858075592767173150807212362100144145460412169544319597424945553719393081684021060397796277295572211805047492475926500818866722386322994857045171241271239312184432717111691471822226211734426321206197761364961297521959398087760034633434420731447302570719084950309779375552351481010459777325573307436315094264376618638582978254557100365396735567006396394469928475016231258524552921462615137659203079579741476093321014818428449064793519514164363883337582004330438807891821403657958108237974905480927931273739083303517970217336187844752434754446452237718809936625698056376227548619851
    n = 341708860755414627517636563737860247694830833438797657665956672468749172737337997411628630654035938329379904059410124228607009461263361069116847161259105255138742079294267425342794529657129825331147410352448839693997261010063688808162779291721751425712075294479847191106434826340717256947538049838702515999605477737814539507461482958208217832001654906428609294670981431708239519975760224167162965883255563080969678819336827357116843767951564821648569178045820428204175762591082444818717364464407951941971606085740333525541803072657460043870118239335947653386353688978688411014446672387410342844504796179832442432516213683576280499042811910325451740078145694525197109311536401111940878021867530800380565979400244930861554608914348506800371272857622124590125877980272975724427805488993427411275730894648138862610811263980653634088749310033841100446125785856461881946689955412063283023124298925564197529712346224365770576932090813671443508185710976892996751059136789460228635799934096464171094867530879063596401568403638549883175241338110538717296368076608313029289635756426606069626131828943894540521046239649485191608386944105862663909092648164662490207600700537314923255529797005890590774810028641986484132364180003123501633206754649
    p_found,q_found = factor(n)
    t1 = time.time()
    print ("n = ", n)
    print ("p = ", p_found)
    print ("q = ", q_found)
    print ("difference abs(p-q) = ", abs(p_found - q_found))
    print ("bit-length n = ", n.bit_length(), " p = ", p_found.bit_length(), " q = ", q_found.bit_length())
    print ("bit length difference (p-q) = ",abs(p_found - q_found).bit_length())
    print ("factorization time =", t1-t0, " seconds")
    # print ("p = ", p)
    # print ("q = ", q)