import { Component } from "@angular/core";
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
} from "@angular/forms";

import { TaskService } from "../services/task.service";

@Component({
  selector: "app-task-form",
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: "./task-form.component.html",
})
export class TaskFormComponent {
  taskForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private taskService: TaskService,
  ) {
    this.taskForm = this.fb.group({
      title: ["", Validators.required],
      description: ["", Validators.required],
    });
  }

  onSubmit(): void {
    if (this.taskForm.valid) {
      const { title, description } = this.taskForm.value;
      this.taskService.addTask(title, description);
      this.taskForm.reset();
    }
  }
}
