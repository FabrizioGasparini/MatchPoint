import {useEffect, useState} from "react";
import api from "../services/api.ts";

import { useNavigate } from 'react-router-dom';

interface Committee {
    id : string;
    name : string;
    title : string;
    address : string;
    email : string;
    phone : string;
    logo : string;
    region : string;
    type : string;
}

const DEFAULT_LOGO = 'https://www.federvolley.it/sites/default/files/FIPAV-orizzontale.png'

const Committees = () => {
    const [committees,
        setCommittees] = useState < Committee[] > ([]);
    const [selectedType,
        setSelectedType] = useState<'t' | 'r' | null>(null);
    
    const navigate = useNavigate();
    
    const handleCardClick = (id: string) => {
        navigate(`/committees/${id}`);
    };

    useEffect(() => {
        const loadCommittees = async() => {
            try {
                const request = (await api.get('/discover/')).data;
                const processedData = request
                    .committees
                    .map((committee : Committee) => ({
                        ...committee,
                        type: committee
                            .name
                            .includes('TERRITORIALE')
                            ? 't'
                            : 'r',
                        region: committee.region
                            .replace("-", " ")
                            .toLowerCase()
                            .split(" ").map((word) => { 
                                return word[0].toUpperCase() + word.substring(1); 
                            }).join(" ")
                    }));
                setCommittees(processedData);
            } catch (err) {
                console.error('Errore durante il caricamento delle federazioni: ', err);
            }
        };

        loadCommittees();
    }, []);

    const filteredCommittees = committees.filter((committee) => committee.type === selectedType);

    const committeesByRegion = filteredCommittees.reduce((acc, committee) => {
        acc[committee.region] = acc[committee.region] || [];
        acc[committee.region].push(committee);
        return acc;
    }, {} as Record < string, Committee[] >);

    const sortedRegions = Object
        .keys(committeesByRegion)
        .sort();

    if (!selectedType) {
        return (
            <div className="flex flex-col items-center w-full justify-center h-5/6 max-h-screen">
                <h1 className="text-7xl font-bold mb-6 text-white">COMITATI</h1>
                <h1 className="text-3xl font-bold mb-6 text-white">Seleziona il tipo di comitato</h1>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-7xl h-full">
                    <div className="relative bg-blue-500 text-white shadow-lg rounded-lg overflow-hidden cursor-pointer hover:scale-105 transform transition"
                        onClick={() => setSelectedType('t')}>
                        <img
                            src="https://fipavbg.it/wp-content/uploads/2023/01/Selezioni2-990x660.jpeg"
                            alt="Comitati Territoriali"
                            className="h-full object-cover opacity-80" />
                        <div className="absolute inset-0 flex items-center justify-center bg-blue-500 bg-opacity-50">
                            <h2 className="text-2xl font-semibold text-white">Comitati Territoriali</h2>
                        </div>
                    </div>
                    <div className="relative bg-green-500 text-white shadow-lg rounded-lg overflow-hidden cursor-pointer hover:scale-105 transform transition"
                        onClick={() => setSelectedType('r')}>
                        <img
                            className="h-full object-cover opacity-80"
                            src="https://www.fipavlazio.net/images/news_cr_lazio/2023/afrogiro.jpg"
                            alt="Comitati Regionali"
                        />
                        <div className="absolute inset-0 flex items-center justify-center bg-green-500 bg-opacity-50">
                            <h2 className="text-2xl font-semibold text-white">Comitati Regionali</h2>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="p-6 w-full min-h-screen">
            <h1 className="text-7xl font-bold mb-6 text-white">COMITATI</h1>
            <button
                className="mb-6 text-blue-400 hover:underline hover:text-blue-300"
                onClick={() => setSelectedType(null)}>
                &larr; Torna indietro
            </button>
            <h1 className="text-3xl font-bold mb-6 text-white">
                {selectedType === 't'
                    ? 'Comitati Territoriali'
                    : 'Comitati Regionali'}
            </h1>
            <div className="flex flex-col items-center justify-center gap-4 mx-10">
                {sortedRegions.map((region) => (
                    <div key={region} className="mb-8 w-full">
                        <h2 className="text-2xl font-semibold text-white mb-4">{region}</h2>
                        <div className="flex flex-wrap justify-center gap-4">
                            {committeesByRegion[region].map((committee) => (
                                <div
                                    key={committee.id}
                                    className={
                                        selectedType == 't'
                                        ? "bg-gray-800 shadow-md rounded-lg overflow-hidden border border-gray-600 flex flex-col items-center hover:scale-105 transform transition w-full md:w-2/5 lg:w-1/3 xl:w-1/5 h-fit"
                                        : "bg-gray-800 shadow-md rounded-lg overflow-hidden border border-gray-600 flex flex-col items-center hover:scale-105 transform transition w-full md:w-1/2 lg:w-1/3 h-fit"
                                    }
                                    onClick={() => handleCardClick(committee.id)}
                                >
                                    <img
                                        src={committee.logo}
                                        alt={committee.title}
                                        className="w-full h-24 py-1 object-contain bg-white"
                                        onError={(e) => (e.currentTarget.src = DEFAULT_LOGO)}
                                    />
                                    <div className="p-2">
                                        <h3 className="text-xl font-semibold text-center text-white">
                                            {
                                                selectedType == 't'
                                                    ? committee.name.split("TERRITORIALE")[1]
                                                    : committee.name.toUpperCase()
                                            }
                                        </h3>
                                    </div>
                                </div>
                            ))}
                            {
                                sortedRegions[sortedRegions.length - 1] != region
                                    ? <span className="w-11/12 bg-gray-600 h-[1px] mt-8"></span>
                                    : ""
                            }
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Committees;
