<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::table('vehicles', function (Blueprint $table) {
            $table->json('raw_status')->nullable();           // stores full JSON
            $table->decimal('batt', 5, 2)->nullable();        // 3.33
            $table->unsignedTinyInteger('left')->default(0);
            $table->unsignedTinyInteger('right')->default(0);
            $table->boolean('highbeam')->default(false);
            $table->boolean('fog')->default(false);
            $table->boolean('hazard')->default(false);
            $table->timestamp('last_seen')->nullable();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('vehicles', function (Blueprint $table) {
            //
        });
    }
};
