import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Task } from "../models/task.model";
import { NotificationService } from "./notification.service";

@Injectable({
  providedIn: "root",
})
export class TaskService {
  private tasks: Task[] = [];
  private tasksSubject = new BehaviorSubject<Task[]>([]);

  //todo: move to config
  private apiUrl = "/api/tasks";

  constructor(
    private http: HttpClient,
    private notificationService: NotificationService,
  ) {
    this.loadTasks();
  }

  getTasks(): Observable<Task[]> {
    return this.tasksSubject.asObservable();
  }

  searchTasks(searchTerm: string): void {
    const filteredTasks = this.tasks.filter(
      (task) =>
        task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        task.description.toLowerCase().includes(searchTerm.toLowerCase()),
    );
    this.tasksSubject.next(filteredTasks);
  }

  filterTasks(filter: string): void {
    let filteredTasks: Task[];
    switch (filter) {
      case "completed":
        filteredTasks = this.tasks.filter((task) => task.completed);
        break;
      case "active":
        filteredTasks = this.tasks.filter((task) => !task.completed);
        break;
      default:
        filteredTasks = [...this.tasks];
    }
    this.tasksSubject.next(filteredTasks);
  }

  addTask(title: string, description: string): void {
    const newTask: Task = {
      title,
      description,
      completed: false,
    };
    this.http.post<Task>(`${this.apiUrl}/`, newTask).subscribe({
      next: (createdTask) => {
        this.notificationService.showSuccess("Task created");
        this.tasks.push(createdTask);
      },
      error: (error) => {
        this.notificationService.showError("Error creating task", error);
      },
    });
  }

  updateTask(task: Task): void {
    this.http.put<Task>(`${this.apiUrl}/`, task).subscribe({
      next: () => {
        this.notificationService.showSuccess("Task updated");
      },
      error: (error) => {
        this.notificationService.showError("Error updating task", error);
      },
    });
  }

  deleteTask(id: string): void {
    this.http.delete(`${this.apiUrl}/${id}`).subscribe({
      next: () => {
        this.tasks = this.tasks.filter((task) => task.id !== id);
        this.notificationService.showSuccess("Task deleted");
      },
      error: (error) => {
        this.notificationService.showError("Error deleting task", error);
      },
    });
  }

  toggleTask(id: string): void {
    const task = this.tasks.find((t) => t.id === id);
    if (task) {
      const updatedTask = { ...task, completed: !task.completed };
      this.http.put<Task>(`${this.apiUrl}/`, updatedTask).subscribe({
        next: () => {
          this.notificationService.showSuccess("Task updated");
          task.completed = !task.completed;
        },
        error: (error) => {
          this.notificationService.showError("Error updating task", error);
        },
      });
    }
  }

  loadTasks(): void {
    this.http.get<Task[]>(`${this.apiUrl}/`).subscribe({
      next: (tasks) => {
        this.tasks = tasks;
        this.updateTasks();
      },
      error: (error) => {
        console.error("Error loading tasks:", error);
      },
    });
  }

  private updateTasks(): void {
    this.tasksSubject.next([...this.tasks]);
  }
}
