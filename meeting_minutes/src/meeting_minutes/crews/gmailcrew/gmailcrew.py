from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .tools.gmail_tool import GmailTool


@CrewBase
class GmailCrew():
	"""Gmailcrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self, session=None):
		self.session = session
		super().__init__()

	@agent
	def gmail_draft_agent(self,session=None) -> Agent:
		return Agent(
			config=self.agents_config['gmail_draft_agent'],
			tools = [GmailTool(session=self.session)],
			verbose=True
		)

	@task
	def gmail_draft_task(self) -> Task:
		return Task(
			config=self.tasks_config['gmail_draft_task'],
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the GmailCrew crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
