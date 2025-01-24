import { Component } from "@angular/core";
import { TaskFormComponent } from "./components/task-form.component";
import { TaskListComponent } from "./components/task-list.component";

@Component({
  selector: "app-root",
  standalone: true,
  imports: [TaskFormComponent, TaskListComponent],
  template: `
    <div class="container mx-auto px-4 py-8 max-w-4xl">
      <app-task-form />
      <app-task-list />
    </div>
  `,
})
export class AppComponent {}
