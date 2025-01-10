import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

import { useNavigate } from 'react-router-dom';
import api from '../services/api';

interface Championship {
    id: string;
    parent: string;
    name: string;
    title: string;
    subtitle: string;
    type: string;
}

const committees = [{"id":"01000","title":"C.R. PIEMONTE"},{"id":"01003","title":"C.T. CUNEO-ASTI"},{"id":"01004","title":"C.T. TICINO SESIA TANARO"},{"id":"01005","title":"C.T. TORINO"},{"id":"01918","title":"Settore Promozionale Torino"},{"id":"02000","title":"C.R. VALLE D'AOSTA"},{"id":"03000","title":"C.R. LIGURIA"},{"id":"03008","title":"C.T. LIGURIA CENTRO"},{"id":"03011","title":"C.T. LIGURIA PONENTE"},{"id":"03104","title":"C.T. LIGURIA LEVANTE"},{"id":"04012","title":"C.T. BERGAMO"},{"id":"04013","title":"C.T. BRESCIA"},{"id":"04014","title":"C.T. COMO"},{"id":"04019","title":"C.T. SONDRIO"},{"id":"04020","title":"C.T. VARESE"},{"id":"08038","title":"C.T. PARMA"},{"id":"09000","title":"C.R. MARCHE"},{"id":"09042","title":"C.T. ANCONA"},{"id":"09043","title":"C.T. ASCOLI PICENO"},{"id":"09044","title":"C.T. MACERATA"},{"id":"09045","title":"C.T. PESARO URBINO"},{"id":"10000","title":"C.R. TOSCANA"},{"id":"10047","title":"C.T. FIRENZE"},{"id":"10051","title":"C.T. APPENNINO TOSCANO"},{"id":"10052","title":"C.T. BASSO TIRRENO"},{"id":"12000","title":"C.R. LAZIO"},{"id":"12057","title":"C.T. FROSINONE"},{"id":"12058","title":"C.T. LATINA"},{"id":"12060","title":"C.T. ROMA"},{"id":"12061","title":"C.T. VITERBO"},{"id":"14000","title":"C.R. ABRUZZO"},{"id":"14067","title":"C.T. ABRUZZO SUD-EST"},{"id":"14068","title":"C.T. ABRUZZO NORD OVEST"},{"id":"17000","title":"C.R. CALABRIA"},{"id":"17080","title":"C.T. CATANZARO"},{"id":"17081","title":"C.T. COSENZA"},{"id":"17082","title":"C.T. REGGIO CALABRIA"},{"id":"18083","title":"C.T. AKRANIS"},{"id":"19000","title":"C.R. SARDEGNA"},{"id":"19092","title":"C.T. CAGLIARI"},{"id":"19093","title":"C.T. CENTRO SARDEGNA"},{"id":"19094","title":"C.T. SASSARI"},{"id":"20000","title":"C.R. MOLISE"},{"id":"04016","title":"C.T. MANTOVA"},{"id":"04018","title":"C.T. PAVIA"},{"id":"05000","title":"C.R. TRENTINO ALTO ADIGE"},{"id":"06000","title":"C.R. VENETO"},{"id":"06024","title":"C.T. PADOVA"},{"id":"06025","title":"C.T. ROVIGO"},{"id":"06026","title":"C.T. TREVISO BELLUNO"},{"id":"06027","title":"C.T. VENEZIA"},{"id":"06028","title":"C.T. VERONA"},{"id":"06029","title":"C.T. VICENZA"},{"id":"07000","title":"C.R. FRIULI VENEZIA GIULIA"},{"id":"07031","title":"C.T. TRIESTE GORIZIA"},{"id":"07032","title":"C.T. UDINE"},{"id":"07033","title":"C.T. PORDENONE"},{"id":"08034","title":"C.T. BOLOGNA"},{"id":"08035","title":"C.T. FERRARA"},{"id":"08039","title":"C.T. PIACENZA"},{"id":"08040","title":"C.T. RAVENNA"},{"id":"08041","title":"C.T. REGGIO EMILIA"},{"id":"08096","title":"C.T. ROMAGNAUNO"},{"id":"11000","title":"C.R. UMBRIA"},{"id":"13000","title":"C.R. CAMPANIA"},{"id":"13062","title":"C.T. IRPINIA SANNIO"},{"id":"13064","title":"C.T. CASERTA"},{"id":"13065","title":"C.T. NAPOLI"},{"id":"13066","title":"C.T. SALERNO"},{"id":"15000","title":"C.R. PUGLIA"},{"id":"15073","title":"C.T. BARI FOGGIA"},{"id":"15076","title":"C.T. LECCE"},{"id":"15077","title":"C.T. TARANTO"},{"id":"16000","title":"C.R. BASILICATA"},{"id":"18000","title":"C.R. SICILIA"},{"id":"18085","title":"C.T. CATANIA"},{"id":"18087","title":"C.T. MESSINA"},{"id":"18088","title":"C.T. PALERMO"},{"id":"18089","title":"C.T. MONTI IBLEI"},{"id":"18091","title":"C.T. TRAPANI"}]
    
function getCommitteeTitleById(id: string) {
    const committee = committees.find(committee => committee.id === id);
    
    return committee?.title || null;
}

const Championships = () => {
    const { id } = useParams<{ id: string }>();
    const [championships, setChampionships] = useState<Championship[]>([]);
    const title = getCommitteeTitleById(id!)

    const [selectedType,
        setSelectedType] = useState<'m' | 'f' | 'x' | null>(null);
    
    const navigate = useNavigate()

    const handleCardClick = (championship_id: string) => {
        navigate(`/committees/${id}/${championship_id}`);
    };

    useEffect(() => {
        const fetchChampionships = async () => {
            try {
                const request = (await api.get(`/discover/${id}`)).data;
                const processedData = request
                    .championships
                    .map((championship: Championship) => ({
                        ...championship,
                        type:
                            championship.parent.toLowerCase().includes('masc')
                                ? 'm'
                                : championship.parent.toLowerCase().includes("femm")
                                    ? 'f'
                                    : 'x',
                    }));
                setChampionships(processedData);
            } catch (err) {
                console.error(err);
                navigate('/committees')
            }
        }

        fetchChampionships()
    }, [id, navigate]);

    const filteredChampionships = championships.filter((championship) => championship.type === selectedType);

    const championshipsByCategory = filteredChampionships.reduce((acc, championship) => {
        acc[championship.parent] = acc[championship.parent] || [];
        acc[championship.parent].push(championship);
        return acc;
    }, {} as Record<string, Championship[]>);

    const sortedChampionships = Object
        .keys(championshipsByCategory)
        .sort();
    
    if (!selectedType) {
        return (
            <div className="flex flex-col items-center w-full justify-center h-5/6 max-h-screen">
                <h1 className="text-7xl font-bold mb-6 text-white">CAMPIONATI - {title}</h1>
                <button
                    className="mb-6 text-blue-400 hover:underline hover:text-blue-300"
                    onClick={() => navigate('/committees')}>
                    &larr; Torna indietro
                </button>
                <h1 className="text-3xl font-bold mb-6 text-white">Seleziona il tipo di campionato</h1>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-7xl h-full">
                    <div className="relative bg-blue-500 text-white shadow-lg rounded-lg overflow-hidden cursor-pointer hover:scale-105 transform transition"
                        onClick={() => setSelectedType('m')}>
                        <img
                            src="https://www.fipavlazio.net/images/news_cr_lazio/2024/coppalaziomaschile2024.jpg"
                            alt="Campionati Maschili"
                            className="h-full object-cover opacity-80" />
                        <div className="absolute inset-0 flex items-center justify-center bg-blue-500 bg-opacity-50">
                            <h2 className="text-2xl font-semibold text-white">Campionati Maschili</h2>
                        </div>
                    </div>
                    <div className="relative bg-pink-500 text-white shadow-lg rounded-lg overflow-hidden cursor-pointer hover:scale-105 transform transition"
                        onClick={() => setSelectedType('f')}>
                        <img
                            className="h-full object-cover opacity-80"
                            src="https://www.federvolley.it/sites/default/files/news/immagini/home%20day%201%20femminile%20tdr.jpg"
                            alt="Campionati Femminili"
                        />
                        <div className="absolute inset-0 flex items-center justify-center bg-pink-500 bg-opacity-50">
                            <h2 className="text-2xl font-semibold text-white">Campionati Femminili</h2>
                        </div>
                    </div>
                    <div className="relative bg-green-500 text-white shadow-lg rounded-lg overflow-hidden cursor-pointer hover:scale-105 transform transition"
                        onClick={() => setSelectedType('x')}>
                        <img
                            className="h-full object-cover opacity-80"
                            src="https://scontent-mxp1-1.cdninstagram.com/v/t39.30808-6/424932056_767778962067051_4091579976405247541_n.jpg?stp=dst-jpg_e35_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi4xMzU0eDEzNTQuc2RyLmYzMDgwOC5kZWZhdWx0X2ltYWdlIn0&_nc_ht=scontent-mxp1-1.cdninstagram.com&_nc_cat=103&_nc_ohc=cHPh8SiWrc0Q7kNvgHiO3-q&_nc_gid=87654c92467e43189ba3e7f1bdec8ef0&edm=APoiHPcAAAAA&ccb=7-5&ig_cache_key=MzMwNjg3ODQzODA2NDE4Mjk5Ng%3D%3D.3-ccb7-5&oh=00_AYAfpw9wJnce0Rhq-3xKbTTU1CJ9c27t_4xMY1jc4ga_sg&oe=67846B45&_nc_sid=22de04"
                            alt="Campionati Misti"
                        />
                        <div className="absolute inset-0 flex items-center justify-center bg-green-500 bg-opacity-50">
                            <h2 className="text-2xl font-semibold text-white">Campionati Misti</h2>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="p-6 w-fit min-h-screen">
            <h1 className="text-7xl font-bold mb-6 text-white">CAMPIONATI - {title}</h1>
            <button
                className="mb-6 text-blue-400 hover:underline hover:text-blue-300"
                onClick={() => setSelectedType(null)}>
                &larr; Torna indietro
            </button>
            <h1 className="text-3xl font-bold mb-6 text-white">
                Campionati
            </h1>
            {Object.entries(championshipsByCategory).map(([parent, championships]) => (
                <div key={parent} className="mb-8 w-full flex flex-col items-center">
                    <h2 className="text-2xl font-semibold text-white mb-4">
                        {parent || 'Senza Categoria'}
                    </h2>
                    <div className="flex flex-wrap items-center justify-center gap-4 mx-10 w-full">
                        {championships.map((championship) => (
                        <div
                            key={championship.id}
                            className="bg-gray-800 shadow-md rounded-lg overflow-hidden border border-gray-700 flex flex-col justify-center items-center hover:scale-105 transform transition w-full md:w-2/5 lg:1/3 xl:w-1/5 h-48 cursor-pointer"
                            onClick={() => handleCardClick(championship.id)}
                        >
                            <div className="p-4 text-center">
                                <h3 className="text-xl font-semibold text-white">{championship.name}</h3>
                                <p className="text-gray-400 text-sm">{championship.subtitle}</p>
                            </div>
                        </div>
                        ))}
                    </div>
                    {
                        sortedChampionships[sortedChampionships.length - 1] != parent
                            ? <span className="w-11/12 h-[1px] bg-gray-600 mt-10"></span>
                            : ""
                    }
                </div>
            ))}
        </div>
    );
};

export default Championships;
