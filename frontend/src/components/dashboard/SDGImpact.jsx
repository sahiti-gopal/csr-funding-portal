import goal1 from "../../../assets/icons/sdg/E-WEB-Goal-01.png";
import goal2 from "../../../assets/icons/sdg/E-WEB-Goal-02.png";
import goal3 from "../../../assets/icons/sdg/E-WEB-Goal-03.png";
import goal4 from "../../../assets/icons/sdg/E-WEB-Goal-04.png";
import goal5 from "../../../assets/icons/sdg/E-WEB-Goal-05.png";
import goal6 from "../../../assets/icons/sdg/E-WEB-Goal-06.png";
import goal7 from "../../../assets/icons/sdg/E-WEB-Goal-07.png";
import goal8 from "../../../assets/icons/sdg/E-WEB-Goal-08.png";
import goal9 from "../../../assets/icons/sdg/E-WEB-Goal-09.png";
import goal10 from "../../../assets/icons/sdg/E-WEB-Goal-10.png";
import goal11 from "../../../assets/icons/sdg/E-WEB-Goal-11.png";
import goal12 from "../../../assets/icons/sdg/E-WEB-Goal-12.png";
import goal13 from "../../../assets/icons/sdg/E-WEB-Goal-13.png";
import goal14 from "../../../assets/icons/sdg/E-WEB-Goal-14.png";
import goal15 from "../../../assets/icons/sdg/E-WEB-Goal-15.png";
import goal16 from "../../../assets/icons/sdg/E-WEB-Goal-16.png";
import goal17 from "../../../assets/icons/sdg/E-WEB-Goal-17.png";

const goals = [
  { id: 1, title: "No Poverty", icon: goal1 },
  { id: 2, title: "Zero Hunger", icon: goal2 },
  { id: 3, title: "Good Health", icon: goal3 },
  { id: 4, title: "Quality Education", icon: goal4 },
  { id: 5, title: "Gender Equality", icon: goal5 },
  { id: 6, title: "Clean Water", icon: goal6 },
  { id: 7, title: "Clean Energy", icon: goal7 },
  { id: 8, title: "Decent Work", icon: goal8 },
  { id: 9, title: "Industry", icon: goal9 },
  { id: 10, title: "Reduced Inequality", icon: goal10 },
  { id: 11, title: "Sustainable Cities", icon: goal11 },
  { id: 12, title: "Responsible Consumption", icon: goal12 },
  { id: 13, title: "Climate Action", icon: goal13 },
  { id: 14, title: "Life Below Water", icon: goal14 },
  { id: 15, title: "Life On Land", icon: goal15 },
  { id: 16, title: "Peace & Justice", icon: goal16 },
  { id: 17, title: "Partnerships", icon: goal17 },
];

export default function SDGImpact() {
  return (
    <div className="sdg-grid">
      {goals.map((goal) => (
        <div
          key={goal.id}
          className="sdg-card"
          title={`${goal.id}. ${goal.title}`}
        >
          <div className="sdg-icon-wrap">
            <img
              src={goal.icon}
              alt={`SDG ${goal.id}: ${goal.title}`}
              className="sdg-icon"
            />
          </div>
          <span className="sdg-caption">{goal.title}</span>
        </div>
      ))}
    </div>
  );
}
