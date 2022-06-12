import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";

import find_agent from "../../assets/find_agent.svg";
import Review from "./Review";
import Stars from "../Tools/Stars";

import { Modal } from "../../context/Modal";
import NewReview from "./Review/NewReview";

import * as agentActions from "../../store/agent";
import * as reviewActions from "../../store/review";

const Agent = () => {
	const dispatch = useDispatch();
	const { agentId } = useParams();
	const agents = useSelector((state) => state.agents);
	const reviews = useSelector((state) => state.reviews);
	const agent = agents[agentId];
	const [showModal, setShowModal] = useState(false);

	const onClose = () => {
		setShowModal(false);
	};

	useEffect(() => {
		dispatch(agentActions.getThisAgent(agentId));
		dispatch(reviewActions.getAllReviews(agentId));
	}, [dispatch]);

	if (agent) {
		return (
			<div className="agent-ctrl">
				<div className="split">
					<div className="center">
						{agent?.photo && (
							<div
								className="photo"
								style={{ backgroundImage: `url("${agent.photo}")` }}
							></div>
						)}

						<div className="name">{agent?.username}</div>
						<div className="office">{agent?.office}</div>
						<div className="license">License # {agent?.license_num}</div>
					</div>
					<div className="bio-wrap">
						<div className="gap15">
							<div className="about">About</div>
							<div className="bio">{agent?.bio}</div>
						</div>
						<div className="gap15">
							<div className="about">Contact</div>
							<div className="phone">Tel {agent?.phone}</div>
							<div className="phone">{agent?.email}</div>
						</div>
						<div>
							Average Rating {agent?.rating} <Stars rating={agent?.rating} />
						</div>
					</div>
				</div>
				<div className="agent-review-ctrl">
					<div className="title">
						<div>Reviews</div>
						<button
							type="button"
							className="btn"
							onClick={() => setShowModal(true)}
						>
							Write a Review
						</button>
					</div>
					{agent && agent?.reviewIds?.length ? (
						<>
							{agent.reviewIds.map((id, idx) => (
								<Review review={reviews[id]} key={"review" + idx} />
							))}
						</>
					) : (
						<div className="review">Be te first to review</div>
					)}
				</div>
				{showModal && (
					<Modal onClose={onClose}>
						<NewReview onClose={onClose} agent={agent} />
					</Modal>
				)}
			</div>
		);
	} else {
		return (
			<div className="agent-404-ctrl">
				<img src={find_agent} alt="404" />
				<div className="title">Sorry! We couldn't find anyone.</div>
				<div className="desc">
					We couldn't find anyone matching your search. Please adjust your
					filters and try again.
				</div>
			</div>
		);
	}
};

export default Agent;