import React, { useState} from 'react';
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
	const [questionNumber, setQuestionNumber] = useState(1);
	const [tabContent, setTabContent] = useState({
		Overall:"",
		City_name:"",
		Climate:"",
		PE:"",
		Infra:"",
		Country:"",
	});


	const handleAnswerOptionClick = (data) => {
		setLoading(true);
		// console.log(currentQuestion);
		// data["questionName"] = currentQuestion.name;
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
			setQuestionNumber(questionNumber + 1);
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
			setQuestionNumber(1);
			setLoading(false);
		});
	}
	if (showResults){
		return (
			<div>
				<MapChart data={resultsData} setTooltipContent={setTabContent}/>
				{
					tabContent ? (
					<ReactTooltip multiline="true">
						Location          				: {tabContent.City_name.charAt(0).toUpperCase() + tabContent.City_name.slice(1)}, {tabContent.Country}
				   <br/>Overall Assessment				: {tabContent.Overall}%
				   <br/>Climate Factors   				: {tabContent.Climate}%
				   <br/>Political and Economic Factors : {tabContent.PE}%
				   <br/>Infrastructure Factors			: {tabContent.Infra}%
				   </ReactTooltip>
					)  : 
					<div>
					</div>
				}
			</div>
		)
	} else {
		return (
			<div className='questions-body'>
			<div className='app'>
				{showIntroduction  ? (
					<div className='introduction-section'>
						<div className='introduction-title'>
							Traveling Recommendations Expert System
						</div>
						< div className='introduction-subtext'>
						Welcome to our traveler recommendations! That web application would help assess potential travel destinations using AI Models in the Backend 😉. Given that our destinations assessment is personalized, you will start by building a personal traveler profile. You will answer a few questions, and then you will get access to an interactive world map to see our assessments. Currently, our systems only support some European Capital cities due to some data availability. Let's get you started!! 
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
								<span>Question {questionNumber}</span>
							</div>
							<div className='question-text'>{currentQuestion.questionText}</div>
						</div>
						{(
								<div className='answer-section'>
									{currentQuestion.answerOptions.map((answerOption) => (
									<button onClick={() => handleAnswerOptionClick({questionName: currentQuestion.name, value: answerOption.value})}>{answerOption.answerText}</button>
									))}
								</div>
						)}
						</> 
					)
				)}
			</div>
			</div>
		);
	}
	}
