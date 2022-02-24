from dataclasses import dataclass
from typing import Dict, List, Tuple
import pprint as pp
import os


@dataclass
class Contributor():
    
    name: str
    num_skills: int
    skills_possessed: Dict[str, int]
    occupied: bool = False


@dataclass(order=True)
class Project():

    best_before: int
    num_days: int
    name: str
    score_for_completion: int
    num_roles: int
    roles: Dict[str, int]


@dataclass
class Parser():

    content: List[str]
    num_contributors: int
    num_projects: int
    current_line: int = 0


    def __init__(self, file_name) -> None:
        with open(file_name, 'r') as f:
            self.content = f.read().splitlines()
        self.num_contributors, self.num_projects = map(int, self.content[0].split())
        self.current_line += 1


    def _read_skills(self, skills_section: List[str]) -> Dict[str, int]:
        skills = {}
        for skill in skills_section:
            skill_name, skill_level = skill.split()
            skills[skill_name] = int(skill_level)
            self.current_line += 1
        return skills


    def _read_contributor_section(self) -> Contributor:
        cont_name, cont_num_skills = self.content[self.current_line].split()
        cont_num_skills = int(cont_num_skills)
        self.current_line += 1
        skills_section = self.content[self.current_line:self.current_line + cont_num_skills]
        skills = self._read_skills(skills_section)
        return Contributor(
            name=cont_name, 
            num_skills=cont_num_skills,
            skills_possessed=skills
        )


    def _read_roles(self, roles_section: List[str]) -> Dict[str, int]:
        roles = {}
        for role in roles_section:
            role_name, role_level = role.split()
            roles[role_name] = int(role_level)
            self.current_line += 1
        return roles


    def _read_project_section(self) -> Project:
        first_line = self.content[self.current_line].split()
        project_name = first_line[0]
        num_days = int(first_line[1])
        score_for_completion = int(first_line[2])
        best_before = int(first_line[3])
        num_roles = int(first_line[4])
        self.current_line += 1
        roles_section = self.content[self.current_line:self.current_line + num_roles]
        roles = self._read_roles(roles_section)
        return Project(
            name=project_name,
            num_days=num_days,
            score_for_completion=score_for_completion,
            best_before=best_before,
            num_roles=num_roles,
            roles=roles
        )


    def read_all_contributor_sections(self) -> List[Contributor]:
        return [self._read_contributor_section() for _ in range(self.num_contributors)]


    def read_all_project_sections(self) -> List[Project]:
        return [self._read_project_section() for _ in range(self.num_projects)]


    def read_all(self) -> Tuple[List[Contributor], List[Project]]:
        contributors = self.read_all_contributor_sections()
        projects = self.read_all_project_sections()
        return contributors, projects


@dataclass
class ProjectHandler():

    projects_to_contributors: Dict[Project, List[Contributor]]
    current_day: int = 0

    def __init__(self, contributors: List[Contributor], projects: List[Project]):
        self.contributors = contributors
        self.projects = projects

    def _assign_contributor(self, contributor: Contributor):
        contributor.occupied = True
        ...

    def assign_contributors(self, project: Project, contributors: List[Contributor]):
        for contributor in contributors:
            self._assign_contributor(contributor)
        self.projects_to_contributors = {project: contributors}

    def score_project(self):
        ...

    def finish_project(self):
        ...


def main():

    file_name = 'a_an_example.in.txt'

    parser = Parser(file_name)

    contributors, projects = parser.read_all()

    schedule_handler = ProjectHandler(contributors, projects)

    pp.pprint(contributors)
    pp.pprint(projects)

    pp.pprint(projects)

    # print(os.listdir())


if __name__ == '__main__':
    main()
