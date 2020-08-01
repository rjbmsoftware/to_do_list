from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def print_menu():
    print("1) Today's tasks",
          "2) Week's tasks",
          '3) All tasks',
          '4) Missed tasks',
          '5) Add task',
          '6) Delete task',
          '0) Exit', sep='\n')


def today_tasks():
    return session.query(Table).filter(Table.deadline == datetime.today()).all()


def print_today_tasks():
    rows = today_tasks()
    print(f'Today {datetime.today().strftime("%d %b")}')
    if rows:
        print(*rows, sep='\n')
    else:
        print('Nothing to do!')
    print()


def add(task_text: str, due_date: datetime) -> None:
    new_row = Table(task=task_text,
                    deadline=due_date)
    session.add(new_row)
    session.commit()


def add_task_interaction():
    print('Enter task')
    task_name = input()
    print('Enter deadline')
    due_date = datetime.strptime(input(), '%Y-%m-%d')
    add(task_name, due_date)


def print_weeks_tasks():
    date_of_task_to_print = datetime.today().date() - timedelta(days=1)
    for i in range(7):
        date_of_task_to_print = date_of_task_to_print + timedelta(days=1)
        print(date_of_task_to_print.strftime('%A %d %b'))
        rows = session.query(Table).filter(Table.deadline == date_of_task_to_print).all()
        if rows:
            print(*rows, sep='\n')
        else:
            print('Nothing to do!')
        print()


def print_all_tasks():
    tasks = session.query(Table).order_by(Table.deadline).all()
    for i in range(len(tasks)):
        due_date = tasks[i].deadline.strftime('%-d %b')
        print(f'{i + 1}. {tasks[i]}. {due_date}')
    print()


def print_missed_tasks():
    tasks = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    print('Missed tasks:')
    if tasks:
        for i in range(len(tasks)):
            due_date = tasks[i].deadline.strftime('%-d %b')
            print(f'{i + 1}. {tasks[i]}. {due_date}')
    else:
        print('Nothing is missed!')
    print()


print_menu()
menu_input = int(input())


def delete_task():
    print('Choose the number of the task you want to delete:')
    tasks = session.query(Table).order_by(Table.deadline).all()
    if tasks:
        for i in range(len(tasks)):
            due_date = tasks[i].deadline.strftime('%-d %b')
            print(f'{i + 1}. {tasks[i]}. {due_date}')
        task_number_to_delete = int(input())
        session.delete(tasks[task_number_to_delete - 1])
        session.commit()
        print('The task has been deleted!')
    else:
        print('Nothing to delete!')
    print()


while menu_input != 0:
    if menu_input == 1:
        print_today_tasks()
    elif menu_input == 2:
        print_weeks_tasks()
    elif menu_input == 3:
        print_all_tasks()
    elif menu_input == 4:
        print_missed_tasks()
    elif menu_input == 5:
        add_task_interaction()
    elif menu_input == 6:
        delete_task()

    print_menu()
    menu_input = int(input())

print('Bye!')
