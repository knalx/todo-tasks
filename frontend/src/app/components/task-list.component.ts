// src/app/components/task-list/task-list.component.ts
import { Component, OnInit } from "@angular/core";
import { AsyncPipe } from "@angular/common";
import { TaskService } from "../services/task.service";
import { WebsocketService } from "../services/websocket.service";
import { Subscription } from "rxjs";
import { Task } from "../models/task.model";

@Component({
  selector: "app-task-list",
  standalone: true,
  imports: [AsyncPipe],
  templateUrl: "./task-list.component.html",
})
export class TaskListComponent implements OnInit {
  messages: any[] = [];
  private messageSubscription: Subscription | undefined;

  tasks$ = this.taskService.getTasks();

  constructor(
    private taskService: TaskService,
    private webSocketService: WebsocketService,
  ) {}

  ngOnInit(): void {
    this.messageSubscription = this.webSocketService
      .getMessages()
      .subscribe((message) => {
        // reload task list on any Collection change
        console.log("Got websocket message - reload tasks");
        this.taskService.loadTasks();
      });
  }

  toggleTask(id: string): void {
    this.taskService.toggleTask(id);
  }

  deleteTask(id: string): void {
    this.taskService.deleteTask(id);
  }

  onSearch(event: Event): void {
    const searchTerm = (event.target as HTMLInputElement).value;
    this.taskService.searchTasks(searchTerm);
  }

  onFilterChange(event: Event): void {
    const filter = (event.target as HTMLSelectElement).value;
    this.taskService.filterTasks(filter);
  }

  ngOnDestroy() {
    // Unsubscribe from WebSocket messages and close the connection
    if (this.messageSubscription) {
      this.messageSubscription.unsubscribe();
    }
    this.webSocketService.closeConnection();
  }
}
