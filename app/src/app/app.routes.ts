import { Routes } from '@angular/router';
import { WealthListComponent } from './components/wealth-list/wealth-list.component';
import { WealthDetailComponent } from './components/wealth-detail/wealth-detail.component';

export const routes: Routes = [
  { path: '', redirectTo: '/wealth', pathMatch: 'full' },
  { path: 'wealth', component: WealthListComponent },
  { path: 'people/:id/wealth', component: WealthDetailComponent },
];
