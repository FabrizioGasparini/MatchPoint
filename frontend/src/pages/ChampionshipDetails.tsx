import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../services/api';
import moment, { Moment } from 'moment';

interface Team {
  id: string;
  logo: string;
  name: string;
  society: string;
  society_id: string;
}

interface Match {
  id: string;
  date: string;
  day: string;
  time: string;
  location: string;
  lat: string;
  lon: string;
  match_number: string;
  played: boolean;
  home_team: Team;
  away_team: Team;
  home_points: number[];
  away_points: number[];
  home_setwin: number;
  away_setwin: number;
}

interface TeamStandings {
  id: string;
  name: string;
  logo: string;
  played: string;
  points: string;
  won_games: string;
  lost_games: string;
  won_sets: string;
  lost_sets: string;
  won_points: string;
  lost_points: string;
  points_ratio: string;
  sets_ratio: string;
  position: number;
}

interface ChampionshipData {
  id: string;
  name: string;
  title: string;
  subtitle: string;
  committee_name: string;
  committee_id: string;
  committee_title: string;
  matches: Match[];
  teams: Team[];
  standings: TeamStandings[];
}

const DEFAULT_IMAGE =
  'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png';

const ChampionshipDetails = () => {
  const { committee_id, id } = useParams<{
    committee_id: string;
    id: string;
  }>();
  const [championshipData, setChampionshipData] = useState<ChampionshipData>(
    {} as ChampionshipData,
  );
  const [activeTab, setActiveTab] = useState('matches');
  const [filters, setFilters] = useState({
    played: 'all',
    team: 'all',
    day: 'all',
    week: '',
  });

  const navigate = useNavigate();

  useEffect(() => {
    const fetchChampionshipData = async () => {
      try {
        const request = await api.get(`/discover/${committee_id}/${id}`);
        const processedData = request.data.championship;
        setChampionshipData(processedData);
      } catch (err) {
        console.error(err);
        navigate(`/committees/${committee_id}`);
      }
    };

    fetchChampionshipData();
  }, [id, committee_id, navigate]);

  if (championshipData.name == undefined)
        return <div className='text-center mt-10'>Caricamento in corso...</div>;
    
    const filteredMatches = Object.values(championshipData.matches).filter((match) => {
        const playedFilter = filters.played || 'all';
        const teamFilter = filters.team || 'all';
        const dayFilter = filters.day || 'all';
        const weekFilter = filters.week || '';

        let selectedWeekStart: Moment | null = null;
        let selectedWeekEnd: Moment | null = null;

        if (weekFilter) {
            selectedWeekStart = moment(weekFilter.replace("-", ""))
            selectedWeekEnd = moment(selectedWeekStart).add(6, 'days');
        }

        const matchDate = moment(match.date.split('/').reverse().join('-'));
        
        const withinWeek = !selectedWeekStart || selectedWeekEnd && moment(matchDate).isBetween(selectedWeekStart, selectedWeekEnd, undefined, "[]");

        const playedCondition = playedFilter === 'all' || (playedFilter === 'played' && match.played) || (playedFilter === 'notPlayed' && !match.played);

        const teamCondition = teamFilter === 'all' || match.home_team.name === teamFilter || match.away_team.name === teamFilter;

        const dayCondition = dayFilter === 'all' || match.day == dayFilter
        
        return playedCondition && teamCondition && withinWeek && dayCondition;
    })

    const orderedMatches = Object.entries(filteredMatches.reduce((days, match) => {
        days[match.day] = days[match.day] || [];
        days[match.day].push(match);
        return days;
    }, {} as Record<string, Match[]>))
  

  return (
    <div className='max-w-6xl mx-auto w-full h-screen p-6 text-white'>
      {/* Intestazione */}
      <div className='mb-6'>
        <h1 className='text-3xl font-bold text-white'>
          {championshipData.name.toUpperCase()}
        </h1>
        <p className='text-sm text-gray-400'>
          <span className='font-medium'>Comitato:</span>{' '}
          {championshipData.committee_name.toUpperCase()}
        </p>
        <button
          className='mt-4 text-blue-400 hover:underline hover:text-blue-300'
          onClick={() => navigate(`/committees/${committee_id}`)}>
          &larr; Torna indietro
        </button>
      </div>

      {/* Tab */}
      <div className='flex border-b border-gray-700 mb-4 items-center justify-center'>
        <button
          onClick={() => setActiveTab('matches')}
          className={`flex-1 px-4 py-2 ${
            activeTab === 'matches'
              ? 'border-b-2 border-blue-500 text-blue-500'
              : 'text-gray-400'
          }`}>
          Gare
        </button>
        <button
          onClick={() => setActiveTab('standings')}
          className={`flex-1 px-4 py-2 ${
            activeTab === 'standings'
              ? 'border-b-2 border-blue-500 text-blue-500'
              : 'text-gray-400'
          }`}>
          Classifica
        </button>
        <button
          onClick={() => setActiveTab('teams')}
          className={`flex-1 px-4 py-2 ${
            activeTab === 'teams'
              ? 'border-b-2 border-blue-500 text-blue-500'
              : 'text-gray-400'
          }`}>
          Squadre
        </button>
      </div>

      {/* Contenuto della Tab */}
      <div>
        {activeTab === 'standings' && (
          <div>
            <h2 className='text-lg font-semibold text-white mb-4'>
              Classifica
            </h2>
            <table className='w-full border border-separate border-gray-700 text-white rounded-xl'>
              <thead className=''>
                <tr>
                  <th className='p-2 text-center bg-gray-900 rounded-tl-xl'>
                    Posizione
                  </th>
                  <th className='p-2 text-center bg-gray-900'>Squadra</th>
                  <th className='p-2 text-center bg-gray-900'>Punti</th>
                  <th className='p-2 text-center bg-gray-900'>Giocate</th>
                  <th className='p-2 text-center bg-gray-900'>Vinte</th>
                  <th className='p-2 text-center bg-gray-900'>Perse</th>
                  <th className='p-2 text-center bg-gray-900'>Set Vinti</th>
                  <th className='p-2 text-center bg-gray-900 rounded-tr-xl'>
                    Set Persi
                  </th>
                </tr>
              </thead>
              <tbody>
                {championshipData.standings.map((standing, index) => (
                  <tr key={index}>
                    <td
                      className={
                        index == championshipData.standings.length - 1
                          ? index % 2 === 0
                            ? 'bg-gray-800 p-2 rounded-bl-xl'
                            : 'bg-gray-700 p-2 rounded-bl-xl'
                          : index % 2 === 0
                            ? 'bg-gray-800 p-2'
                            : 'bg-gray-700 p-2'
                      }>
                      {standing.position}
                    </td>
                    <td
                      className={
                        index % 2 === 0 ? 'bg-gray-800 p-2' : 'bg-gray-700 p-2'
                      }>
                      {standing.name}
                    </td>
                    <td
                      className={
                        index % 2 === 0 ? 'bg-gray-800 p-2' : 'bg-gray-700 p-2'
                      }>
                      {standing.points}
                    </td>
                    <td
                      className={
                        index % 2 === 0 ? 'bg-gray-800 p-2' : 'bg-gray-700 p-2'
                      }>
                      {standing.played}
                    </td>
                    <td
                      className={
                        index % 2 === 0 ? 'bg-gray-800 p-2' : 'bg-gray-700 p-2'
                      }>
                      {standing.won_games}
                    </td>
                    <td
                      className={
                        index % 2 === 0 ? 'bg-gray-800 p-2' : 'bg-gray-700 p-2'
                      }>
                      {standing.lost_games}
                    </td>
                    <td
                      className={
                        index % 2 === 0 ? 'bg-gray-800 p-2' : 'bg-gray-700 p-2'
                      }>
                      {standing.won_sets}
                    </td>
                    <td
                      className={
                        index == championshipData.standings.length - 1
                          ? index % 2 === 0
                            ? 'bg-gray-800 p-2 rounded-br-xl'
                            : 'bg-gray-700 p-2 rounded-br-xl'
                          : index % 2 === 0
                            ? 'bg-gray-800 p-2'
                            : 'bg-gray-700 p-2'
                      }>
                      {standing.lost_sets}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'matches' && (
            <div>
                <h2 className='text-lg font-semibold text-white mb-4'>Gare</h2>

                {/* Filtri */}
                <div className='mb-6 p-4 bg-gray-800 rounded-lg'>
                    <h3 className='text-md font-semibold text-gray-300 mb-2'>
                        Filtra le Partite
                    </h3>
                    <div className='grid grid-cols-1 sm:grid-cols-3 md:grid-cols-3 xl:grid-cols-4 gap-4'>
                        <div>
                            <label className='block text-gray-400 text-sm mb-1'>
                                Giocata
                            </label>
                            <select
                                className='w-full p-2 rounded bg-gray-700 text-white'
                                onChange={(e) => {
                                    setFilters({
                                        played: e.target.value,
                                        week: filters.week,
                                        team: filters.team,
                                        day: filters.day
                                    });
                                }}>
                                <option value='all'>Tutte</option>
                                <option value='played'>Giocate</option>
                                <option value='notPlayed'>Non Giocate</option>
                            </select>
                        </div>
                        <div>
                            <label className='block text-gray-400 text-sm mb-1'>
                                Squadra
                            </label>
                            <select
                                id='teamFilter'
                                className='w-full p-2 rounded bg-gray-700 text-white'
                                onChange={(e) => {
                                    setFilters({
                                        team: e.target.value,
                                        played: filters.played,
                                        week: filters.week,
                                        day: filters.day
                                    });
                                }}>
                                <option value='all'>Tutte</option>
                                {[
                                    ...new Set(
                                        championshipData.matches.flatMap((match) => [
                                            match.home_team.name,
                                            match.away_team.name,
                                        ]),
                                    ),
                                ]
                                    .sort()
                                    .map((teamName) => (
                                        <option key={teamName} value={teamName}>
                                            {teamName}
                                        </option>
                                    ))}
                            </select>
                        </div>
                        <div>
                            <label className='block text-gray-400 text-sm mb-1'>
                                Giornata
                            </label>
                            <select
                                id='dayFilter'
                                className='w-full p-2 rounded bg-gray-700 text-white'
                                onChange={(e) => {
                                    setFilters({
                                        team: filters.team,
                                        played: filters.played,
                                        week: filters.week,
                                        day: e.target.value
                                    });
                                }}>
                                <option value='all'>Tutte</option>
                                {[...new Set(Object.values(championshipData.matches).flatMap(match=>match.day))]
                                    .map((day) => (
                                        <option key={day} value={day}>
                                            {day}
                                        </option>
                                    ))}
                            </select>
                        </div>
                        <div>
                            <label className='block text-gray-400 text-sm mb-1'>
                                Data
                            </label>
                            <input
                                type='week'
                                id='weekFilter'
                                className='w-full p-2 rounded bg-gray-700 text-white'
                                onChange={(e) => {
                                    setFilters({
                                        team: filters.team,
                                        played: filters.played,
                                        week: e.target.value,
                                        day: filters.day
                                    });
                                }}
                            />
                        </div>
                    </div>
                </div>

                {/* Gare divise per giornata */}
                {orderedMatches.map(([day, matches]) => (
                    <div key={day} className='mb-6'>
                    <h3 className='text-4xl font-semibold text-blue-400 mb-4'>
                        {day}
                    </h3>
                    <ul>
                        {matches.map((match, index) => (
                        <li key={index} className="mb-4 p-4 border rounded-lg bg-gray-800">
                            <p className=" text-blue-400">
                                <strong>{match.day}</strong> - <span className=''>Partita #{match.match_number}</span>
                            </p>
                            <p className="text-gray-400">
                                <strong>Data e Ora:</strong> {match.date}, {match.time}
                            </p>
                            <p className="text-gray-400">
                                <strong>Luogo: </strong>
                                <a href={"https://www.google.com/maps/search/?api=1&query=" + match.lat.replace(",", ".") + "," + match.lon.replace(",", ".")} target='_blank' className='text-gray-200 hover:underline'>{match.location}</a>    
                            </p>
                            <div className="flex justify-between items-center  mt-4">
                                <div className="flex items-center justify-start w-2/5">
                                    <img
                                        src={match.home_team.logo}
                                        alt={match.home_team.name}
                                        className="w-10 h-10 mr-2 rounded-full"
                                    />
                                    <span className="text-white text-nowrap text-ellipsis w-1/2 text-left ml-5">{match.home_team.name}</span>
                                </div>
                                <div className="text-lg font-bold text-gray-200 w-1/5">
                                {match.played
                                    ? `${match.home_setwin} - ${match.away_setwin}`
                                    : "Non giocata"}
                                </div>
                                <div className="flex items-center justify-end w-2/5">
                                <span className="text-white text-nowrap text-ellipsis w-1/2 mr-5 text-right">{match.away_team.name}</span>
                                <img
                                    src={match.away_team.logo}
                                    alt={match.away_team.name}
                                    className="w-10 h-10 mr-2 rounded-full"
                                />
                                </div>
                            </div>
                            {match.home_points.length != 0 && (
                                <div className="mt-4">
                                <div className='flex flex-col items-center justify-center'>
                                    <strong>Punti: </strong>
                                    <p className='flex gap-8 items-center justify-center text-gray-400 w-fit'>
                                        {
                                            match.home_points.map((_, index) => (
                                                <span key={index} className='flex-1 w-fit text-nowrap'>{ + _} - {match.away_points[index]}</span>    
                                            ))
                                        }        
                                    </p>
                                </div>
                                </div>
                            )}
                            </li>
                        ))}
                    </ul>
                    </div>
                ))}
          </div>
        )}

        {activeTab == 'teams' && (
          <div>
            <h2 className='text-lg font-semibold text-white mb-4'>
              Squadre Partecipanti
            </h2>
            <ul className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4'>
              {championshipData.standings.map((standing, index) => (
                <li
                  key={index}
                  className='relative w-full h-40 [transform-style:preserve-3d] [perspective:1000px] group'>
                  <div className='w-full h-full transition-transform duration-500 [transform-style:preserve-3d] group-hover:[transform:rotateY(180deg)] relative'>
                    {/* Front Side */}
                    <div className='absolute w-full h-full bg-gray-800 text-white rounded-lg flex flex-col items-center justify-center [backface-visibility:hidden]'>
                      <img
                        src={standing.logo}
                        alt={standing.name}
                        onError={(e) => (e.currentTarget.src = DEFAULT_IMAGE)}
                        className='w-12 h-12 rounded-full mb-2'
                      />
                      <p>{standing.name}</p>
                    </div>

                    {/* Back Side */}
                    <div className='absolute w-full h-full bg-gray-700 text-gray-300 rounded-lg flex flex-col items-start justify-center px-4 [backface-visibility:hidden] [transform:rotateY(180deg)]'>
                      <p>
                        <strong>Partite Giocate:</strong> {standing.played}
                      </p>
                      <p>
                        <strong>Punti Totali:</strong> {standing.points}
                      </p>
                      <p>
                        <strong>Set Vinti:</strong> {standing.won_sets} |{' '}
                        <strong>Set Persi:</strong> {standing.lost_sets}
                      </p>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChampionshipDetails;