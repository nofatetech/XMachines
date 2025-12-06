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
        Schema::create('machines', function (Blueprint $table) {
            $table->id();
            $table->uuid('uuid')->unique();
            $table->string('name');
            $table->string('small_description')->nullable();
            $table->text('description')->nullable();
            $table->boolean('is_active')->default(true);
            $table->decimal('temperature', 5, 2)->nullable();
            $table->boolean('is_online')->default(false);
            $table->integer('motor_left_speed')->default(0);
            $table->integer('motor_right_speed')->default(0);
            $table->boolean('lights_on')->default(false);
            $table->boolean('fog_lights_on')->default(false);

            $table->integer('happiness')->default(50);
            $table->integer('hunger')->default(0);
            $table->boolean('is_auto_driving')->default(false);

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('machines');
    }
};
