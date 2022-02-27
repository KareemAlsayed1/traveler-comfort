import React, { useState } from 'react';
import RingLoader from "react-spinners/RingLoader";
import MapChart from "./MapChart";
import ReactTooltip from "react-tooltip";


export default function App() {
	const [currentQuestion, setCurrentQuestion] = useState({
		name : "",
		questionText: "",
		answerOptions: []
	});
	const [showIntroduction, setShowIntroduction] = useState(true);
	const [loading, setLoading] = useState(false);
	const [showResults, setShowResults] = useState(false);
	const [resultsData, setResultsData] = useState({});
	const [tabContent, setTabContent] = useState("");

	
	const handleAnswerOptionClick = (data) => {
		setLoading(true);
		const fetchAPI = '/questions/next-question/';
		fetch(fetchAPI, {
			method: 'POST',
			body: JSON.stringify(data),
			headers: {
				'Content-Type': 'application/json',
			  }
		})
		  .then(res => res.json())
		  .then(data => {
			  if (data["data"]["type"] === "question"){
				setCurrentQuestion(data["data"]["data"]);
				setShowResults(false);
			  } else if (data["data"]["type"] === "results"){
				setResultsData(data["data"]["data"][0]);
				console.log(data["data"]["data"][0]);
				setShowResults(true);
			  }
		}).finally(() => {
			setLoading(false);
		});
	};

	const handleStartClick = () =>{
		setLoading(true);
		setShowIntroduction(false);
		getStarted();
	}
	const getStarted = () => {
		const fetchAPI = '/questions/next-question';
		fetch(fetchAPI, {method: 'DELETE'})
		  .then(res => res.json())
		  .then(data => {
			if (data["data"]["type"] === "question"){
				setCurrentQuestion(data["data"]["data"]);
				setShowResults(false);
			  } else if (data["data"]["type"] === "results"){
				setResultsData(data["data"]["data"][0]);
				console.log(data["data"]["data"][0]);
				setShowResults(true);
			  }
		}).finally(() => {
			setLoading(false);
		});
	}
	if (showResults){
		return (
			<div>
				<MapChart data={resultsData} setTooltipContent={setTabContent}/>
				<ReactTooltip>{tabContent}</ReactTooltip>
			</div>
		)
	} else{
		return (
			<div className='questions-body'>
			<div className='app'>
				{/* <button onClick={getQuestions}>hhhh</button> */}
				{showIntroduction  ? (
					<div className='introduction-section'>
						<div className='introduction-title'>
							Traveling Recommendations Expert System
						</div>
						< div className='introduction-subtext'>
							It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over.
						</div>
						<button className='start-button' onClick={handleStartClick}>
							<span>Let's get started!</span>
						</button> 
					</div>
				) : ( loading ? (
					<>
						<div className='loading-section'>
							<RingLoader color={"#FFFFFF"} loading={loading} size={120} css={"align-self: center;"}/>
							<div className="loading-text">Running our AI Models!</div>
						</div>
					</> ) : (
						<>
						<div className='question-section'>
							<div className='question-count'>
								<span>Question {1}</span>
							</div>
							<div className='question-text'>{currentQuestion.questionText}</div>
						</div>
						<div className='answer-section'>
							{currentQuestion.answerOptions.map((answerOption) => (
								<button onClick={() => handleAnswerOptionClick({questionName: currentQuestion.name, value: answerOption.value})}>{answerOption.answerText}</button>
							))}
						</div>
						</> 
					)
				)}
			</div>
			</div>
		);
	}
	}
