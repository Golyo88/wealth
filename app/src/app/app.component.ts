import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { WealthListComponent } from './components/wealth-list/wealth-list.component';
import { WealthDetailComponent } from './components/wealth-detail/wealth-detail.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    WealthListComponent,
    WealthDetailComponent,
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {}
