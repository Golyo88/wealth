import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { WealthService } from '../../services/wealth.service';
import { Wealth } from '../../models/wealth.model';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-wealth-detail',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './wealth-detail.component.html',
  styleUrls: ['./wealth-detail.component.scss'],
})
export class WealthDetailComponent implements OnInit {
  wealth: Wealth | null = null;
  loading = false;

  constructor(
    private route: ActivatedRoute,
    private wealthService: WealthService
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loading = true;
      this.wealthService.findById(id).subscribe({
        next: (response) => {
          this.wealth = response;
        },
        error: (error) => {
          console.error('Hiba történt:', error);
        },
        complete: () => {
          this.loading = false;
        },
      });
    }
  }
}
